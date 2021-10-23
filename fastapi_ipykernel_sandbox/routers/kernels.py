from functools import lru_cache
from pathlib import Path
from typing import Dict, List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Response, status
from jupyter_client.connect import LocalPortCache, write_connection_file
from jupyter_client.kernelspec import find_kernel_specs, get_kernel_spec
from jupyter_client.provisioning import (KernelProvisionerBase,
                                         KernelProvisionerFactory)

from ..constants import ROOT_DIR
from ..models.kernels import Kernel

router = APIRouter()

kernel_factory = KernelProvisionerFactory()


@lru_cache
def connection_file_dir() -> Path:
    data_dir = ROOT_DIR / ".connection-files"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@lru_cache
def kernel_spec():
    spec_name = list(find_kernel_specs().keys())[0]
    return get_kernel_spec(spec_name)


KERNEL_CACHE: Dict[str, KernelProvisionerBase] = {}


@router.post("/kernels", status_code=status.HTTP_201_CREATED, response_model=Kernel)
async def create_kernel(connection_file_dir=Depends(connection_file_dir)):
    # https://github.com/jupyter/jupyter_client/blob/master/jupyter_client/provisioning/factory.py
    kernel_id = str(uuid4())
    provisioner = kernel_factory.create_provisioner_instance(
        kernel_id, kernel_spec(), None
    )
    KERNEL_CACHE[kernel_id] = provisioner
    kwargs = await provisioner.pre_launch(independent=True)
    kernel_cmd = kwargs.pop("cmd")
    ip = "0.0.0.0"
    lpc = LocalPortCache.instance()
    connection_info = dict(
        shell_port=lpc.find_available_port(ip),
        iopub_port=lpc.find_available_port(ip),
        stdin_port=lpc.find_available_port(ip),
        control_port=lpc.find_available_port(ip),
        hb_port=lpc.find_available_port(ip),
    )
    file_path = str((connection_file_dir / f"{kernel_id}.json").resolve())
    for idx in range(0, len(kernel_cmd)):
        arg = kernel_cmd[idx]
        if arg == "{connection_file}":
            kernel_cmd[idx] = file_path
    write_connection_file(file_path, **connection_info, ip=ip)
    provisioner.connection_info = connection_info
    await provisioner.launch_kernel(kernel_cmd, **kwargs)
    return Kernel(id=kernel_id, connection_info_file=file_path)


@router.get("/kernels", status_code=status.HTTP_200_OK, response_model=List[Kernel])
async def get_kernels(connection_file_dir=Depends(connection_file_dir)):
    return [
        Kernel(
            id=id,
            connection_info_file=str((connection_file_dir / f"{id}.json").resolve()),
        )
        for id, kernel in KERNEL_CACHE.items()
    ]


@router.get("/kernels/{id}", status_code=status.HTTP_200_OK, response_model=Kernel)
async def get_kernel(id: str, connection_file_dir=Depends(connection_file_dir)):
    kernel = KERNEL_CACHE.get(id)
    if kernel is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Kernel(
        id=id, connection_info_file=str((connection_file_dir / f"{id}.json").resolve())
    )


@router.delete("/kernels/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kernel(id: str, connection_file_dir=Depends(connection_file_dir)):
    kernel = KERNEL_CACHE.get(id)
    if kernel is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    await kernel.terminate(restart=False)
    await kernel.cleanup(restart=False)
    del KERNEL_CACHE[id]
    file_path: Path = (connection_file_dir / f"{id}.json").resolve()
    file_path.unlink()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

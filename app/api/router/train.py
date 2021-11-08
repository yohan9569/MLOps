import multiprocessing
import os
import re
import subprocess

from fastapi import APIRouter

from app.utils import (
    ExperimentOwl,
    NniWatcher,
    base_dir,
    get_free_port,
    write_yml,
)
# download_autowebglm_model.py
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="THUDM/autowebglm-6b",
    local_dir="modals/AutoWebGLM/models/autowebglm-6b",
    local_dir_use_symlinks=False
)

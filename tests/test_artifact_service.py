from pathlib import Path

from app.models.generated_artifcats import Generated_Artifact
from app.services.artifact_service import ArtifactService


def test_save_artifact(tmp_path):

    service = ArtifactService()

    artifact = Generated_Artifact(
        filename="login.html",
        artifact_type="HTML",
        description="Login page",
        content="<html></html>",
    )

    service.save(
        [artifact],
        output_dir=tmp_path,
    )

    saved_file = tmp_path / "login.html"

    assert saved_file.exists()

    assert saved_file.read_text() == "<html></html>"
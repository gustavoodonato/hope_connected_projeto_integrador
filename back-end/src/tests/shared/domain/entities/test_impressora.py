import pytest
from pydantic import ValidationError

from src.shared.domain.entities.impressora import Impressora
from src.shared.domain.entities.volume_impressao import VolumeImpressao
from src.shared.domain.enums.status_disponibilidade_enum import StatusDisponibilidadeEnum
from src.shared.domain.enums.tecnologia_impressora_enum import TecnologiaImpressoraEnum
from src.shared.helpers.errors.domain_errors import EntityError


@pytest.fixture
def volume():
    return VolumeImpressao(x_mm=220, y_mm=220, z_mm=250)


@pytest.fixture
def dados_validos(volume):
    return dict(
        id_usuario_fornecedor=456,
        marca_modelo="Creality Ender 3 V2",
        tecnologia=TecnologiaImpressoraEnum.FDM,
        volume_impressao=volume,
    )


class Test_Impressora:
    def test_impressora_creation_success(self, volume):
        impressora = Impressora(
            id=10,
            id_usuario_fornecedor=456,
            marca_modelo="Creality Ender 3 V2",
            tecnologia=TecnologiaImpressoraEnum.FDM,
            volume_impressao=volume,
            status_disponibilidade=StatusDisponibilidadeEnum.EM_USO,
        )
        assert impressora.id == 10
        assert impressora.id_usuario_fornecedor == 456
        assert impressora.marca_modelo == "Creality Ender 3 V2"
        assert impressora.tecnologia == TecnologiaImpressoraEnum.FDM
        assert impressora.volume_impressao.x_mm == 220
        assert impressora.volume_impressao.y_mm == 220
        assert impressora.volume_impressao.z_mm == 250
        assert impressora.status_disponibilidade == StatusDisponibilidadeEnum.EM_USO

    def test_impressora_default_values(self, dados_validos):
        impressora = Impressora(**dados_validos)
        assert impressora.id == 0
        assert impressora.status_disponibilidade == StatusDisponibilidadeEnum.DISPONIVEL

    def test_impressora_accepts_enum_values_as_string(self):
        impressora = Impressora(
            id_usuario_fornecedor=456,
            marca_modelo="Anycubic Photon",
            tecnologia="SLA",
            volume_impressao={"x_mm": 192, "y_mm": 120, "z_mm": 245},
            status_disponibilidade="Inativa",
        )
        assert impressora.tecnologia == TecnologiaImpressoraEnum.SLA
        assert impressora.status_disponibilidade == StatusDisponibilidadeEnum.INATIVA
        assert impressora.volume_impressao.z_mm == 245

    def test_impressora_marca_modelo_is_stripped(self, dados_validos):
        dados_validos["marca_modelo"] = "   Bambu Lab P1S   "
        impressora = Impressora(**dados_validos)
        assert impressora.marca_modelo == "Bambu Lab P1S"

    def test_impressora_without_marca_modelo(self, dados_validos):
        del dados_validos["marca_modelo"]
        with pytest.raises(EntityError):
            Impressora(**dados_validos)

    def test_impressora_blank_marca_modelo(self, dados_validos):
        dados_validos["marca_modelo"] = "    "
        with pytest.raises(EntityError):
            Impressora(**dados_validos)

    def test_impressora_marca_modelo_too_long(self, dados_validos):
        dados_validos["marca_modelo"] = "A" * 121
        with pytest.raises(EntityError):
            Impressora(**dados_validos)

    def test_impressora_without_id_usuario_fornecedor(self, dados_validos):
        del dados_validos["id_usuario_fornecedor"]
        with pytest.raises(EntityError):
            Impressora(**dados_validos)

    @pytest.mark.parametrize("id_invalido", [0, -1])
    def test_impressora_invalid_id_usuario_fornecedor(self, dados_validos, id_invalido):
        dados_validos["id_usuario_fornecedor"] = id_invalido
        with pytest.raises(EntityError):
            Impressora(**dados_validos)

    def test_impressora_without_tecnologia(self, dados_validos):
        del dados_validos["tecnologia"]
        with pytest.raises(EntityError):
            Impressora(**dados_validos)

    def test_impressora_invalid_tecnologia(self, dados_validos):
        dados_validos["tecnologia"] = "TECNOLOGIA_INVALIDA"
        with pytest.raises(EntityError):
            Impressora(**dados_validos)

    def test_impressora_invalid_status_disponibilidade(self, dados_validos):
        dados_validos["status_disponibilidade"] = "STATUS_INVALIDO"
        with pytest.raises(EntityError):
            Impressora(**dados_validos)

    def test_impressora_without_volume_impressao(self, dados_validos):
        del dados_validos["volume_impressao"]
        with pytest.raises(EntityError):
            Impressora(**dados_validos)

    def test_impressora_invalid_volume_impressao(self, dados_validos):
        dados_validos["volume_impressao"] = {"x_mm": 0, "y_mm": 220, "z_mm": 250}
        with pytest.raises(EntityError):
            Impressora(**dados_validos)

    def test_impressora_extra_field_forbidden(self, dados_validos):
        dados_validos["campo_inexistente"] = "x"
        with pytest.raises(EntityError):
            Impressora(**dados_validos)

    def test_impressora_is_immutable(self, dados_validos):
        impressora = Impressora(**dados_validos)
        with pytest.raises(ValidationError):
            impressora.status_disponibilidade = StatusDisponibilidadeEnum.INATIVA


class Test_VolumeImpressao:
    def test_volume_creation_success(self):
        volume = VolumeImpressao(x_mm=192, y_mm=120.5, z_mm=245)
        assert volume.x_mm == 192
        assert volume.y_mm == 120.5
        assert volume.z_mm == 245

    @pytest.mark.parametrize("campo", ["x_mm", "y_mm", "z_mm"])
    @pytest.mark.parametrize("valor", [0, -10])
    def test_volume_non_positive_dimension(self, campo, valor):
        dados = {"x_mm": 220, "y_mm": 220, "z_mm": 250}
        dados[campo] = valor
        with pytest.raises(ValidationError):
            VolumeImpressao(**dados)

    @pytest.mark.parametrize("campo", ["x_mm", "y_mm", "z_mm"])
    def test_volume_missing_dimension(self, campo):
        dados = {"x_mm": 220, "y_mm": 220, "z_mm": 250}
        del dados[campo]
        with pytest.raises(ValidationError):
            VolumeImpressao(**dados)

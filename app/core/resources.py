from import_export import resources
from core import models

class ContractResources(resources.ModelResource):
    class Meta:
        model = models.Contracts
        import_id_fields  = ("contract_number",)

from core.driver.ansible.form.adhoc_result import AdHocResult
from core.service import DriverService
from server.apps.ansible.forms.playbook import PlaybookModel


class AnsiblePlaybookService(DriverService):
    __driver_tag__ = "ansible"
    driver_run_fn = "run_playbook"
    input_model = PlaybookModel
    output_model = AdHocResult

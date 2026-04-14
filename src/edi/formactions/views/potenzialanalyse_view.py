# from edi.formactions import _
import json

from edi.formactions.views.annotations_view import AnnotationsView
from zope.interface import implementer
from zope.interface import Interface
from Products.Five.browser import BrowserView

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IPotenzialanalyseView(Interface):
    """Marker Interface for IPotenzialanalyseView"""


mapping = {
    "not": "Nicht relevant",
    "ready": "Bereits angeboten",
    "standard": "Soll der Standardweg sein",
    "important": "Wichtig für die Realisierung",
    "condition": "Notwendige Bedingung für die Realisierung",
}


def create_service(json_data: dict) -> dict:
    return {
        "service_id": json_data.get("service_id", ""),
        "service_title": json_data.get("service_title", "")
        or json_data.get("service_title_new", ""),
        "service_description": json_data.get("service_description_new", ""),
        "mandant": json_data.get("mandant", ""),
        "bearbeitung_durch": json_data.get("bearbeitung_durch", ""),
        "fachbereich": json_data.get("fachbereich", ""),
        "status": json_data.get("status", ""),
        "fachdomaene": json_data.get("fachdomaene", ""),
        "fachbereich_subdomaene": json_data.get("mub_fachbereich", "")
        or json_data.get("subdomaenen_rul", "")
        or json_data.get("subdomaenen_praev", ""),
        "querschnittsthemen": json_data.get("querschnittsthemen", ""),
        "list_potenziale": json_data.get("list_potenziale", ""),
        "potenziale_weitere": json_data.get("potenziale_weitere", ""),
        "browser": mapping.get(json_data.get("browser", ""), ""),
        "app_pwa": mapping.get(json_data.get("app_pwa", ""), ""),
        "api": mapping.get(json_data.get("api", ""), ""),
        "chatbot": json_data.get("chatbot", ""),
        "ki_assistenz": json_data.get("ki_assistenz", ""),
        "automatisierung": json_data.get("automatisierung", ""),
        "aufwand": json_data.get("aufwand", ""),
        "ideen": json_data.get("ideen", ""),
    }
    # servicelandkarte_ja_nein ?
    # funktion ?


@implementer(IPotenzialanalyseView)
class AnnotationsPotenzialanalyseView(AnnotationsView):
    """
    View for a form (IForm) that contains annotations with the form data of the filled form (created by the formaction annotation_storage_handler)
    """

    def __call__(self):
        return self.index()

    def get_services(self):
        annotations = self.get_annotations()
        services = []
        for annotation in annotations:
            json_data = annotation["json_data"]
            service = create_service(json_data)
            services.append(service)
        return services


@implementer(IPotenzialanalyseView)
class JFDPotenzialanalyseView(BrowserView):
    """
    View for a folder that contains JsonFormsDocuments (created by the formaction file_storage_handler)
    """

    def __call__(self):
        return self.index()

    def get_services(self):
        jfds = self.context.restrictedTraverse("contentlisting")()
        services = []
        for jfd in jfds:
            if jfd.portal_type != "JsonFormsDocument":
                continue
            json_data_str = getattr(jfd, "json_data", "{}")
            json_data = json.loads(json_data_str)
            service = create_service(json_data)
            services.append(service)
        return services

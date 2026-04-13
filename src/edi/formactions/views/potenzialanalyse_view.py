# -*- coding: utf-8 -*-

# from edi.formactions import _
from edi.formactions.views.annotations_view import AnnotationsView
from zope.interface import implementer
from zope.interface import Interface

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


@implementer(IPotenzialanalyseView)
class PotenzialanalyseView(AnnotationsView):
    def __call__(self):
        return self.index()

    def get_services(self):
        annotations = self.get_annotations()
        services = []
        for annotation in annotations:
            annotation = annotation["json_data"]
            import pdb

            pdb.set_trace()
            service = {
                "service_id": annotation.get("service_id", ""),
                "service_title": annotation.get("service_title", "")
                or annotation.get("service_title_new", ""),
                "service_description": annotation.get("service_description_new", ""),
                "mandant": annotation.get("mandant", ""),
                "bearbeitung_durch": annotation.get("bearbeitung_durch", ""),
                "fachbereich": annotation.get("fachbereich", ""),
                "status": annotation.get("status", ""),
                "fachdomaene": annotation.get("fachdomaene", ""),
                "fachbereich_subdomaene": annotation.get("mub_fachbereich", "")
                or annotation.get("subdomaenen_rul", "")
                or annotation.get("subdomaenen_praev", ""),
                "querschnittsthemen": annotation.get("querschnittsthemen", ""),
                "list_potenziale": annotation.get("list_potenziale", ""),
                "potenziale_weitere": annotation.get("potenziale_weitere", ""),
                "browser": mapping.get(
                    annotation.get("browser", ""), ""
                ),  # map to bedeutung_kommunikationskanaele
                "app_pwa": mapping.get(annotation.get("app_pwa", ""), ""),
                "api": mapping.get(annotation.get("api", ""), ""),
                "chatbot": annotation.get("chatbot", ""),
                "ki_assistenz": annotation.get("ki_assistenz", ""),
                "automatisierung": annotation.get("automatisierung", ""),
                "aufwand": annotation.get("aufwand", ""),
                "ideen": annotation.get("ideen", ""),
            }
            # servicelandkarte_ja_nein ?
            # funktion ?
            services.append(service)
        return services

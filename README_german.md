This documentation is currently only available in german.

Um die Daten eines Fragebogens mit Buttons zu verarbeiten, muss zunächst eine Button Gruppe hinzugefügt werden. Der Titel und die Beschreibung der Button Gruppe und aller folgenden Artikeltypen werden nicht im Fragebogen verwendet.

Eine Button Gruppe dient als Container, der beliebig viele Buttons enthalten kann. Es gibt zwei Arten von Buttons: den Reset-Button zum Zurücksetzen des Fragebogens, und einen Button, zur Verarbeitung der Formulardaten. Bei beiden Buttons kann man die Beschriftung und die Farbvariante anpassen. Beim normalen Button kann zusätzlich noch eine URL angegeben werden, die nach der erfolgreichen Verarbeitung aufgerufen wird.

Die Funktionalität eines normalen Buttons, also die Verarbeitung der Formulardaten, wird über Handler gesteuert. Liegt in einem Button ein Handler, so wird dieser beim Klick auf den Button ausgeführt, sofern es keine Validierungsfehler gibt (z. B. wenn ein Pflichtfeld nicht ausgefüllt ist). Liegen in einem Button mehrere Handler, so werden diese einer nach dem anderen, in genau der Reihenfolge, in der sie im Button liegen, ausgeführt. Schlägt die Aktion eines Handlers fehl, werden auch die Aktionen der darauffolgenden Handler nicht mehr durchgeführt.

Mögliche Handler im Button sind:
- Annotation Storage Handler
- File Storage Handler
- E-Mail-Handler
- Webservice-Handler

Die Aktion eines Annotation Storage Handlers ist das Speichern der Formulardaten im Plone Annotation Storage des jeweiligen Fragebogens. Die gespeicherten Daten können über das Ändern der Darstellung des Fragebogens angesehen werden. Dazu muss die Darstellung des Fragebogens auf "Annotationen" geändert werden.

Ein File Storage Handler speichert die Daten des Fragebogens im angegebenen Zielordner. Diese Objekte sind nur für den Ersteller (also den Nutzer, der den Fragebogen abgesendet hat) und für Administratoren sichtbar (Status "privat"). Die Ansicht dieser Objekte ähnelt dem des Fragebogens mit dem Unterschied, dass die Buttons ersetzt wurden, um ein Bearbeiten der Formulardaten ausschließlich für den Ersteller zu ermöglichen. Der Titel, mit dem die Formulardaten-Objekte gespeichert werden, kann konfiguriert werden. Diese Definition kann auch dynamisch und abhängig von den eingegebenen Daten sein, indem mit Jinja2-Logik auf die IDs des/der Feldes/er im Fragebogen verwiesen wird (siehe Beschreibung des Feldes "Titel für die gespeicherten Objekte"). Schlägt die Auswertung dieser Definition fehl (z. B. weil auf ein Feld verwiesen wird, dass kein Pflichtfeld ist und das nicht ausgefüllt wurde), hat das gespeicherte Objekt den Standardtitel "Formularübermittlung".

Mit einem E-Mail-Handler werden die Formulardaten an eine angegebene E-Mail-Adresse gesendet. Statt einer festen E-Mail-Adresse kann auch die Option aktiviert werden, dass an den aktuellen Nutzer, der den Fragebogen ausgefüllt hat, eine E-Mail mit den Formulardaten gesendet wird. Man kann den Betreff und den E-Mail-Text, der den Formulardaten vorangestellt wird, konfigurieren. Soll sowohl an eine feste E-Mail-Adresse als auch an den angemeldeten Nutzer eine E-Mail gesendet werden, müssen zwei E-Mail-Handler erstellt werden.

Der Webservice-Handler kann mehrere Endpunkte enthalten, an die jeweils die Formulardaten übermittelt werden. Pro Endpunkt muss die URL und können ein API-Key inklusive Header-Name angegeben werden.
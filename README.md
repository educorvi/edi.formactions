# edi.formactions

[![Build Status](https://github.com/educorvi/edi.formactions/actions/workflows/plone-package.yml/badge.svg)](https://github.com/educorvi/edi.formactions/actions/workflows/plone-package.yml)
[![PyPI Version](https://img.shields.io/pypi/v/edi.formactions.svg)](https://pypi.python.org/pypi/edi.formactions/)
[![License](https://img.shields.io/pypi/l/edi.formactions.svg)](https://pypi.python.org/pypi/edi.formactions/)

> **Disclaimer:** This README was generated with the assistance of AI.

`edi.formactions` is a [Plone](https://plone.org) add-on that provides form action buttons and handlers for [edi.jsonforms](https://github.com/educorvi/edi.jsonforms). It enables JSON Forms embedded in Plone to submit data via email, store it inside the Plone site (as annotations or content objects), or forward it to external web services.

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Content Types](#content-types)
  - [Button Group](#button-group)
  - [Button](#button)
  - [Reset Button](#reset-button)
  - [Email Handler](#email-handler)
  - [Annotation Storage Handler](#annotation-storage-handler)
  - [File Storage Handler](#file-storage-handler)
  - [Webservice Handler](#webservice-handler)
  - [Endpoint](#endpoint)
  - [JsonForms Document](#jsonforms-document)
- [Content Hierarchy](#content-hierarchy)
- [REST API Endpoints](#rest-api-endpoints)
- [Configuration Options](#configuration-options)
- [Translations](#translations)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

`edi.formactions` extends the `edi.jsonforms` package by adding configurable form action objects directly inside the Plone content tree. Editors can build complex form-submit workflows entirely through the Plone backend without writing code:

- **Group buttons** inside a Button Group and attach multiple independent handlers to each button.
- **Send email notifications** when a form is submitted.
- **Store submissions** as Plone annotations on the form object (lightweight, no extra content objects created).
- **Save submissions as content objects** (`JsonFormsDocument`) in a designated folder, with Jinja2-templated titles.
- **Forward submissions to external web services** via HTTP POST, optionally authenticated with an API key.
- **Reset the form** with a dedicated Reset Button.

---

## Requirements

| Requirement | Notes |
|---|---|
| Plone 5.2 or 6.0 | Both versions are supported |
| Python ≥ 3.7 | |
| [`edi.jsonforms`](https://github.com/educorvi/edi.jsonforms) | Provides the `Form` content type and JSON schema/UI schema views that this package builds upon |
| [`plone.restapi`](https://github.com/plone/plone.restapi) | REST API endpoints are registered as `plone.restapi` services |
| [`plone.app.dexterity`](https://github.com/plone/plone.app.dexterity) | Dexterity content type framework |
| [`plone.api`](https://github.com/plone/plone.api) ≥ 1.8.4 | Plone API helpers |
| [`z3c.jbot`](https://github.com/malthe/z3c.jbot) | Template override support |
| [`Jinja2`](https://jinja.palletsprojects.com/) | Used for rendering dynamic content object titles in the File Storage Handler |

The `plone.restapi` and `plone.app.dexterity` GenericSetup profiles are declared as dependencies and are installed automatically.

---

## Installation

1. Add `edi.formactions` to your buildout or pip environment:

   **buildout (`buildout.cfg`)**
   ```ini
   [buildout]
   eggs =
       edi.formactions
   ```
   Then run `bin/buildout`.

   **pip**
   ```bash
   pip install edi.formactions
   ```

2. Install the add-on through the Plone control panel (*Site Setup → Add-ons*) or via the command line using `plone.cli` / `instance run`.

---

## Content Types

### Button Group

A container that groups one or more buttons together. The Button Group is rendered as a row of buttons at the bottom of a JSON form.

**Allowed children:** `Button`, `Reset Button`

| Field | Type | Required | Description |
|---|---|---|---|
| *(inherited from plone.basic)* | | | Title and description |

---

### Button

A submit button. When clicked, every handler placed inside it executes its action in order.

**Allowed children:** `Email Handler`, `File Storage Handler`, `Annotation Storage Handler`, `Webservice Handler`

| Field | Type | Required | Description |
|---|---|---|---|
| `button_label` | Text line | Yes | Label displayed on the button. Default: *"Send request(s)"* |
| `button_variant` | Choice | Yes | Bootstrap colour variant (vocabulary `plone.app.widgets.buttons:BUTTON_VARIANTS`). Default: `primary` |
| `page_after_success` | URI | No | URL to redirect the user to after all handlers have executed successfully |

---

### Reset Button

A button that clears all fields in the form without submitting data.

| Field | Type | Required | Description |
|---|---|---|---|
| `button_label` | Text line | Yes | Label displayed on the button. Default: *"Reset form"* |
| `button_variant` | Choice | Yes | Bootstrap colour variant. Default: `danger` |

---

### Email Handler

Sends the form submission data to a specified email address.

| Field | Type | Required | Description |
|---|---|---|---|
| `use_email_of_current_user` | Boolean | No | When checked, the currently logged-in user's email address is used as the recipient instead of the value in `to_address` |
| `to_address` | Text line | Conditional | Recipient email address. Required when `use_email_of_current_user` is unchecked |
| `email_subject` | Text line | No | Subject line of the outgoing email |
| `email_text` | Text | No | Body text prepended to the form data in the email |

> **Note:** The sender address is read from the Plone registry record `plone.email_from_address`. Configure it under *Site Setup → Mail*.

**Validation invariants:**
- `to_address` is required when `use_email_of_current_user` is `False`.
- `to_address` must be empty when `use_email_of_current_user` is `True`.

---

### Annotation Storage Handler

Stores form submission data as a persistent annotation on the form content object. Submissions are appended to a `PersistentList` stored under the annotation key `edi.formactions.annotations`.

This handler has no additional configuration fields beyond the standard Plone fields (`title`, `description`).

> **Tip:** Access stored annotations programmatically via `edi.formactions.annotations.FormActionsAnnotationStorage(context).get_all_annotations()`.

---

### File Storage Handler

Saves each form submission as a `JsonFormsDocument` content object inside a designated Plone folder. The created object is automatically set to the `private` workflow state and can only be edited by its creator or a user with *Modify portal content* permission.

| Field | Type | Required | Description |
|---|---|---|---|
| `target_folder` | Relation (Folder) | Yes | The Plone folder where submitted `JsonFormsDocument` objects will be created |
| `content_object_title` | Text line | No | Jinja2 template for the title of created objects. Available variables: `data` (dict of submitted form field values by field ID), `user` (user ID of the submitter or `"anonymous"`). Example: `Form submission from {{data['first_name']}} on {{data['date']}}` |

> **Note:** If the target folder is deleted, the button will be disabled.

---

### Webservice Handler

Forwards form submission data (as JSON) via HTTP POST to all `Endpoint` objects placed inside it.

This handler has no additional configuration fields. Add one or more `Endpoint` child objects to configure target URLs.

**Allowed children:** `Endpoint`

---

### Endpoint

Configures a single HTTP POST target for a Webservice Handler.

| Field | Type | Required | Description |
|---|---|---|---|
| `url` | URI | Yes | The URL to which the form data will be sent |
| `api_key_header_name` | Text line | No | The HTTP header name used to transmit the API key (e.g. `X-Api-Key`) |
| `api_key` | Text line | No | The API key value sent in the header defined by `api_key_header_name` |

---

### JsonForms Document

A content object that stores a single JSON form submission. It is created automatically by the **File Storage Handler** and is not meant to be created manually.

| Field | Type | Required | Description |
|---|---|---|---|
| `json_data` | Text | Yes | The JSON-encoded form submission data |
| `json_schema` | Text | Yes | The JSON schema of the form at the time of submission |
| `ui_schema` | Text | Yes | The UI schema of the form at the time of submission (button groups are stripped and replaced with a single *Save* button) |

---

## Content Hierarchy

Below is a typical content structure inside an `edi.jsonforms` **Form** object:

```
Form (edi.jsonforms)
└── Button Group
    ├── Button ("Submit")
    │   ├── Email Handler
    │   ├── Annotation Storage Handler
    │   ├── File Storage Handler
    │   └── Webservice Handler
    │       ├── Endpoint ("My API")
    │       └── Endpoint ("Backup API")
    └── Reset Button ("Clear form")
```

All button/handler content types have `global_allow = False`, meaning they can only be created inside the appropriate parent objects and do not appear in the general *Add content* menu.

---

## REST API Endpoints

All services are registered as `plone.restapi` services and are available on the URL of the `edi.jsonforms` **Form** object (or `JsonFormsDocument` for the edit endpoint).

| Method | URL pattern | Permission | Description |
|---|---|---|---|
| `GET` | `{form_url}/@form_actions` | `zope2.View` | Returns form action metadata. Supports `expand=true` to include full action details. |
| `POST` | `{form_url}/@send-email` | `zope2.View` | Sends the form data as an email. Parameters are read from the `Email Handler` content object. |
| `POST` | `{form_url}/@webservice-request` | `zope2.View` | Forwards form data to configured endpoints. Endpoint URLs and API keys are passed as request headers (`endpoint-1-url`, `endpoint-1-api-key-header-name`, `endpoint-1-api-key`, etc.). |
| `POST` | `{form_url}/@store-as-annotation` | `zope2.View` | Stores form data as an annotation on the form object. |
| `POST` | `{form_url}/@store-as-file` | `zope2.View` | Stores form data as a `JsonFormsDocument` in a target folder. Accepts `folder_path`, `content_object_title`, and `page_after_success` as form parameters. |
| `POST` | `{document_url}/@edit-jsonformsdocument` | `zope2.View` | Updates the `json_data` field of an existing `JsonFormsDocument`. Only the creator of the object (or a user with *Modify portal content*) may call this. |

All POST endpoints read the form submission from the request **body** as a JSON string and disable CSRF protection (`IDisableCSRFProtection`) to allow cross-origin form submissions.

---

## Configuration Options

`edi.formactions` does not currently define any custom registry records of its own. Configuration is handled through the content objects described above and through the standard Plone configuration described below.

### Plone Registry

| Registry record | Location in control panel | Description |
|---|---|---|
| `plone.email_from_address` | *Site Setup → Mail* | Default sender ("From") address used when the Email Handler sends emails |

Configure this record via the Plone control panel or programmatically:

```python
from plone import api
api.portal.set_registry_record('plone.email_from_address', 'noreply@example.com')
```

### GenericSetup Profile

The default GenericSetup profile (`profile-edi.formactions:default`) installs the following:

- All Dexterity content type definitions (FTIs) for the content types listed above.
- A browser layer (`IEdiFormactionsLayer`) that scopes views and services to sites where the add-on is installed.
- Role map entries.
- Catalog index configuration.
- Dependencies on `profile-plone.app.dexterity:default` and `profile-plone.restapi:default`.

---

## Translations

The package ships with translation catalogues for:

- **English** (`en`)
- **German** (`de`)

Translation strings use the `edi.formactions` i18n domain. To update or add translations, use the included `update_locale` console script:

```bash
bin/update_locale
```

---

## Contributing

- **Issue Tracker:** https://github.com/educorvi/edi.formactions/issues
- **Source Code:** https://github.com/educorvi/edi.formactions

Pull requests are welcome. Please ensure existing tests pass before submitting.

### Running Tests

```bash
bin/test
```

---

## License

This project is licensed under the [GNU General Public License v2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

---

*This README was generated with the assistance of AI.*

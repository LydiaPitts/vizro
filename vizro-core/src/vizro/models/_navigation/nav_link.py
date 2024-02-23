from __future__ import annotations

import itertools

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html

try:
    from pydantic.v1 import Field, PrivateAttr, validator
except ImportError:  # pragma: no cov
    from pydantic import Field, PrivateAttr, validator

from vizro.models import VizroBaseModel
from vizro.models._models_utils import _log_call
from vizro.models._navigation._navigation_utils import _validate_pages
from vizro.models._navigation.accordion import Accordion
from vizro.models.types import NavPagesType


class NavLink(VizroBaseModel):
    """Icon that serves as a navigation link to be used in navigation bar of Dashboard.

    Args:
        pages (NavPagesType): See [`NavPagesType`][vizro.models.types.NavPagesType]. Defaults to `[]`.
        label (str): Text description of the icon for use in tooltip.
        icon (str): Icon name from [Google Material icons library](https://fonts.google.com/icons). Defaults to `""`.

    """

    pages: NavPagesType = []
    label: str = Field(..., description="Text description of the icon for use in tooltip.")
    icon: str = Field("", description="Icon name from Google Material icons library.")
    _nav_selector: Accordion = PrivateAttr()

    # Re-used validators
    _validate_pages = validator("pages", allow_reuse=True)(_validate_pages)

    @validator("icon")
    def validate_icon(cls, icon) -> str:
        return icon.strip().lower().replace(" ", "_")

    @_log_call
    def pre_build(self):
        from vizro.models._navigation.accordion import Accordion

        self._nav_selector = Accordion(pages=self.pages)

    @_log_call
    def build(self, *, active_page_id=None):
        # _nav_selector is an Accordion, so _nav_selector._pages is guaranteed to be Dict[str, List[str]].
        # `active_page_id` is still required here for the automatic opening of the Accordion when navigating
        # from homepage to a page within the Accordion and there are several Accordions within the page.
        all_page_ids = list(itertools.chain(*self._nav_selector.pages.values()))
        first_page_id = all_page_ids[0]
        item_active = active_page_id in all_page_ids

        try:
            first_page = dash.page_registry[first_page_id]
        except KeyError as exc:
            raise KeyError(
                f"Page with ID {first_page_id} cannot be found. Please add the page to `Dashboard.pages`"
            ) from exc

        nav_link = dbc.NavLink(
            [
                dmc.Tooltip(
                    label=self.label,
                    offset=4,
                    withArrow=True,
                    children=[html.Span(self.icon, className="material-symbols-outlined")],
                    position="bottom-start",
                    className="nav-icon-tooltip",
                )
            ],
            id=self.id,
            className="nav-bar-icon-link",
            href=first_page["relative_path"],
            # `active` is required to keep the icon highlighted when navigating through different pages inside
            # the nested accordion
            active=item_active,
        )

        # Only build the nav_selector (id="nav-panel") if the item is active.
        if item_active:
            return html.Div([nav_link, self._nav_selector.build(active_page_id=active_page_id)])

        # html.Div required to access the nav_link via ID
        return html.Div(nav_link)

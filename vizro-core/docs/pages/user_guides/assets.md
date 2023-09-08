# How to add static assets

This guide shows you how to add static assets to your dashboard. Static assets are images that you would like to show in your dashboard, or custom CSS and JS files
with which you would like to enhance/change the appearance of your dashboard.

To add images, custom CSS or JS files, create a folder named `assets` in the root of your app directory and insert your files.
Assets included in that folder are automatically served after serving Vizro's static files via the `external_stylesheets`  and `external_scripts` arguments of [Dash](https://dash.plotly.com/external-resources#adding-external-css/javascript).
The user-provided `assets` folder thus always takes precedence.

```text title="Example folder structure"
├── app.py
├── assets
│   ├── css
│       ├── **/*.css
│   ├── images
│       ├── icons
│           ├── collections.svg
├── favicon.ico
```

## Adding static images
We leverage Dash's underlying functionalities to embed images into the app.
For more information, see [here](https://dash.plotly.com/dash-enterprise/static-assets?de-version=5.1#embedding-images-in-your-dash-apps).

For example, you can leverage the `dash.get_asset_url()` function in your custom components, such that any provided path does not require `assets` as a prefix in the relative path anymore.


## Changing the favicon
To change the default favicon (website icon appearing in the browser tab), add a file named `favicon.ico` to your `assets` folder.
For more information, see [here](https://dash.plotly.com/external-resources#changing-the-favicon).

## Overwriting CSS properties
To overwrite any CSS properties of existing Vizro components, target the right CSS property and place your CSS files in the `assets` folder. This will overwrite any existing defaults for that CSS property.
For reference, all Vizro CSS files can be found [here](pages.md).

!!! example "Customising CSS"
    === "my_css_file.css"
    ```css
    h1, h2 {
     color: hotpink;
    }
    ```
    === "app.py"
        ```py
        import vizro.models as vm
        from vizro import Vizro

        page = vm.Page(
                title="Changing the header color",
                components=[
                    vm.Card(
                        text="""

                            # This is an <h1> tag

                            ## This is an <h2> tag

                            ###### This is an <h6> tag
                        """)
                    ],
                )

        dashboard = vm.Dashboard(pages=[page])

        Vizro().build(dashboard).run()
        ```
    === "app.yaml"
        ```yaml
        # Still requires a .py to register data connector in Data Manager and parse yaml configuration
        # See from_yaml example
        pages:
        - components:
            - text: |
                # This is an <h1> tag

                ## This is an <h2> tag

                ###### This is an <h6> tag
              type: card
          title: Changing the header color
        ```
    === "Result"
         [![AssetsCSS]][AssetsCSS]

    [AssetsCSS]: ../../assets/user_guides/assets/css_change.png

???+ note

    CSS properties will be applied with the last served file taking precedence.
    Files are served in alphanumerical order.

    **Order of CSS being served to app**

    1. Dash styling sheets
    2. Vizro external styling sheets
    3. User assets folder
        - CSS/JS Files
        - Folders
           - CSS/JS Files

## Changing the `assets` folder path
If you do not want to place your `assets` folder in the root directory of your app, you can
also change the reference to your `assets` folder. Note that the path provided needs to be an absolute path.

```python
from vizro import Vizro
import vizro.models as vm

page = <INSERT CONFIGURATION HERE>
dashboard = vm.Dashboard(pages=[page])

Vizro._user_assets_folder = "absolute/path/to/assets"
app = Vizro().build(dashboard).run()

```

Note that in the example above, you still need to configure your [`Page`][vizro.models.Page].
A guide on how to do that you can find [here](https://github.com/mckinsey/vizro/blob/main/docs/pages/user_guides/pages.md)
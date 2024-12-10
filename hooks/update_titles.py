import logging
import mkdocs.plugins

log = logging.getLogger('mkdocs')

def set_page_icon(page, config, component_type=None):
    icons = config.get('theme').get('icon').get('tag', {})
    page.meta['icon'] = icons.get(component_type, None)
    page.meta['tags'] = [component_type] + page.meta.get('tags', [])

# https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown
@mkdocs.plugins.event_priority(-50)
def on_page_markdown(markdown, page, config, **kwargs):
    path = page.file.src_uri
    
    if any(keyword in path for keyword in ["SCSTG-TEST-", "SCSTG-TOOL-", "SCSTG-TECH-", "SCSTG-APP-", "SCSTG-DEMO-", "SCSTG-MITIG-"]):
        # TODO the component ID is the file basename without the extension; ensure that all components have id in the future
        page.meta['id'] = path.split('/')[-1].split('.')[0]
        component_type = page.meta['id'].split('-')[1].lower()
        page.meta['title'] = f"{page.meta['id']}: {page.meta.get('title', '')}"

        set_page_icon(page, config, component_type)

        page.meta['hide'] = ['toc']

    if page.meta.get('id') and "SCWE" in page.meta.get('id'): 
        page.meta['title'] = f"{page.meta.get('id')}: {page.meta.get('title', '')}"
        component_type = "scwe"
        set_page_icon(page, config, component_type)
    
        page.meta['hide'] = ['toc']
    
    return markdown

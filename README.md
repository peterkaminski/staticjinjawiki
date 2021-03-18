# Static Jinja Wiki

Generate HTML pages from Markdown wiki pages.

Needs a `.staticjinjawiki` directory at the top level of your Markdown wiki directory.

In the `.staticjinjawiki` directory, create a page template called `page.html`.

Here is a start:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Our Wiki</title>
  </head>
  <body>
    {{ post_content_html }}
  </body>
</html>
```

Run SJW like this.

```shell
./sjw.py -d path-to-our-wiki
```

HTML pages will be generated into `.staticjinjawiki/output`.


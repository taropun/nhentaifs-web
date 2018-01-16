<!DOCTYPE HTML>
<html lang="en">
  <head>
    <meta charset="utf-8">
    % if defined('title'):
    <title>nhentaifs - {{title}}</title>
    % else:
    <title>nhentaifs</title>
    % end
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />
  </head>
  <body>
    <main>
      {{!base}}
    </main>
    % if defined('scripts'):
    % for script in scripts:
      <script type="text/javascript" src="{{script}}"></script>
    % end
    % end
  </body>
</html>

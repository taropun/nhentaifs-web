% rebase('base.html.tpl', scripts=['/static/js/prefetcher.js', '/static/js/gallerykeys.js'])

% include('navbar.html.tpl')

<section class="page">
  % if nav['next']:
    <a href="{{base}}{{nav['next']}}">
      <img id="page__image" src="{{page_url}}" />
    </a>
  % else:
    <a href="{{gallery_url}}">
      <img id="page__image" src="{{page_url}}" />
    </a>
  % end
</section>

% include('navbar.html.tpl')
<section id="gallery__link">
  <a href="{{gallery_url}}">Back to gallery</a>
</section>

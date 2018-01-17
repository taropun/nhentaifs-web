% rebase('base.html.tpl')

% include('search.html.tpl')

% include('navbar.html.tpl')

<section class="page">
  % if nav['next']:
    <a href="{{base}}{{nav['next']}}">
      <img class="page__image" src="{{page_url}}" />
    </a>
  % else:
    <a href="{{gallery_url}}">
      <img class="page__image" src="{{page_url}}" />
    </a>
  % end
</section>

% include('navbar.html.tpl')
<section class="gallery__link">
  <a href="{{gallery_url}}">Back to gallery</a>
</section>

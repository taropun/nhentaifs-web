% rebase('base.html.tpl', scripts=['/static/js/lazyload.js'])

% include('search.html.tpl')

<section class="metadata">
  <img class="metadata__cover" src="/img/{{metadata['cover']}}" />
  <div class="metadata__details">
    <h2>{{metadata['title']['english']}}</h2>
    <h3>{{metadata['title']['native']}}</h3>
    <div class="metadata__details__tags">
      % for key, tags in metadata['tags'].items():
        <div class="metadata__details__tags__tag">
          <span class="metadata__details__tags__tag__name">{{key}}</span>:
          % for ID, value in tags.items():
            <a href="/tagged/{{ID}}">{{value}}</a>
          % end
        </div>
      % end
    </div>
    <div class="metadata__details__misc">
      {{metadata['num_pages']}} pages<br />
      Uploaded {{metadata['uploaded']}}
    </div>
  </div>
</section>

<section class="galleries">
  % for row in thumbs:
    <div class="lazyload galleries__row">
      % for i, thumb in row:
        <div class="galleries__row__col">
          <a class="galleries__row__col__thumb"
             href="/gallery/{{metadata['id']}}/{{i + 1}}">
            <img class="galleries__row__col__thumb"
                 data-src="{{thumb}}"
                 src="/static/img/thumb_placeholder.gif" />
            <noscript>
              <img class="galleries__row__col__thumb" src="{{thumb}}" />
            </noscript>
          </a>
        </div>
      % end
    </div>
  % end
</section>

<section class="related">
  <h2>Related galleries</h2>
  <div class="galleries__row">
    % for gallery in related:
      <div class="galleries__row__col">
        <a class="galleries__row__col__thumb"
           href="/gallery/{{gallery['id']}}">
          <img class="lazyload galleries__row__col__thumb"
               src="/img/{{gallery['cover']}}" />
        </a>
        <span class="galleries__row__col__label">
          <a href="/gallery/{{gallery['id']}}">
            {{gallery['title']}}
          </a>
        </span>
      </div>
    % end
  </div>
</section>

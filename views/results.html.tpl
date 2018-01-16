% rebase('base.html.tpl')

% include('search.html.tpl')

<section class="galleries">
  % for row in galleries:
    <div class="galleries__row">
      % for gallery in row:
        <div class="galleries__row__col">
          <a class="galleries__row__col__thumb"
             href="/gallery/{{gallery['id']}}">
            <img class="galleries__row__col__thumb"
                 title="{{gallery['title']}}"
                 src="/img/{{gallery['thumb']}}" />
          </a>
          <span class="galleries__row__col__label">
            <a href="/gallery/{{gallery['id']}}">
              {{gallery['title']}}
            </a>
          </span>
        </div>
      % end
    </div>
  % end
</section>

% include('navbar.html.tpl')

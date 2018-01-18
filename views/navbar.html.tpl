<section class="navbar">
  % if nav['previous']:
    <a class="navbar__first" href="{{base}}{{nav['first']}}">«</a>
    <a class="navbar__prev" rel="prev" href="{{base}}{{nav['previous']}}">‹</a>
  % end
  % if 'window' in nav:
    % for page in nav['window']:
      % if page == nav['current']:
        <span class="navbar_page navbar__current">{{page}}</span>
      % else:
        <a class="navbar__page" href="{{base}}{{page}}">{{page}}</a>
      % end
    % end
  % else:
    <span class="navbar__current">{{nav['current']}}</span>
    /
    <span class="navbar__last">{{nav['last']}}</span>
  % end
  % if nav['next']:
    <a class="navbar__next" rel="next" href="{{base}}{{nav['next']}}">›</a>
    <a class="navbar__last" href="{{base}}{{nav['last']}}">»</a>
  % end
</section>

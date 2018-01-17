(function() {
  'use strict';

  function elementInViewport(element) {
    var rect = element.getBoundingClientRect();
    var windowEnd = window.innerHeight || document.documentElement.clientHeight;
    if (rect.top < 0) {
      return -1;
    } else if (rect.top > windowEnd) {
      return 1;
    } else {
      return 0;
    }
  }

  function findItem(items, predicate) {
    var low = 0;
    var high = items.length - 1;

    while ((high - low) > 1) {
      var mid = (low + high) >>> 1;
      if (predicate(items[mid])) {
        high = mid;
      } else {
        low = mid;
      }
    }

    if (predicate(items[high])) {
      return high;
    } else {
      throw "Couldn't find item"
    }
  }

  function firstTruthyItem(items, comparator) {
    if (comparator(items[0]) === 0) {
      return 0;
    }

    return findItem(items, function(x) {
      return comparator(x) >= 0;
    });
  }

  function lastTruthyItem(items, comparator) {
    if (comparator(items[items.length - 1]) === 0) {
      return items.length;
    }

    return findItem(items, function(x) {
      return comparator(x) > 0;
    });
  }

  function truthyItems(items, comparator) {
    if (items.length === 0) {
      return [];
    }

    var low = firstTruthyItem(items, comparator);
    var high = lastTruthyItem(items, comparator);
    return Array.prototype.slice.call(items, low, high);
  }

  function lazyload(e) {
    var rows = document.querySelectorAll('.lazyload.galleries__row');
    var visibleRows = truthyItems(rows, elementInViewport);

    for (var i = 0; i < visibleRows.length; i++) {
      var row = visibleRows[i];
      var thumbs = row.querySelectorAll('img');
      for (var j = 0; j < thumbs.length; j++) {
        var thumb = thumbs[j];
        thumb.src = thumb.getAttribute('data-src');
      }
      row.classList.remove('lazyload');
    }
  }

  document.addEventListener('scroll', lazyload);
  lazyload();
})();

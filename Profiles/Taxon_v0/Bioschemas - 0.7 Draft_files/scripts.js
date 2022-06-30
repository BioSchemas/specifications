/**
 * Enabling Clipboard
 */

var clipboard = new ClipboardJS('.btn-copy')

clipboard.on('success', function (e) {
  var tooltipBtn = bootstrap.Tooltip.getInstance(e.trigger)

  e.trigger.setAttribute('data-bs-original-title', 'Copied!')
  tooltipBtn.show()

  e.trigger.setAttribute('data-bs-original-title', 'Copy to clipboard')
})

/**
 * Function to open external links in separate tab
 */
 $(document).ready(function external_new_window() {
  for (var c = document.getElementsByTagName("a"), a = 0; a < c.length; a++) {
    var b = c[a];
    if (b.getAttribute("href") && b.hostname !== location.hostname) {
      b.target = "_blank";
      b.rel = "noopener";
    }
  }
});


/**
 * Heading animation
 */

$(window).scroll(function () {
  var topOfDiv = $('#header_wrap').offset().top;
  var height = $('#header_wrap').outerHeight();
  if ($(window).width() > 700) {
    if ($(window).scrollTop() > (topOfDiv + height)) {
      $(".trigger").addClass("stuck");
      $("#header_wrap").addClass("stuck");
    } else {
      $(".trigger").removeClass("stuck");
      $("#header_wrap").removeClass("stuck");
    }
  }
});

/**
 * Enabling deep linking towards tabs
 */

$(document).ready(() => {
  let url = location.href.replace(/\/$/, "");

  if (location.hash) {
    const hash = url.split("#")
    newhash = hash[1].split("?row=");
    $('button[data-bs-target="#' + newhash[0] + '"]').tab("show");
    url = location.href.replace(/\/#/, "#");
    history.replaceState(null, null, url);
    setTimeout(() => {
      $(window).scrollTop(0);
    }, 400);
  }

  $('button[data-bs-toggle="tab"]').on("click", function () {
    let newUrl;
    const hash = $(this).attr("data-bs-target");
    newUrl = url.split("#")[0] + hash;
    history.replaceState(null, null, newUrl);
  });
});

/**
 * Enabling deep linking towards rows in accordion
 */

 $(document).ready(() => {
  let url = location.href.replace(/\/$/, "");
  if (location.hash) {
    const hash = url.split("?row=");
    $('button[data-bs-target="#' + hash[1] + '"]').trigger('click');
  }
});

/**
 * Topnav over headings fix
 */

(function (document, history, location) {
  var HISTORY_SUPPORT = !!(history && history.pushState);
  var anchorScrolls = {
    ANCHOR_REGEX: /^#[^ ]+$/,
    OFFSET_HEIGHT_PX: 54,
    init: function () {
      this.scrollToCurrent();
      $(window).on('hashchange', $.proxy(this, 'scrollToCurrent'));
      $('body').on('click', 'a', $.proxy(this, 'delegateAnchors'));
    },
    getFixedOffset: function () {
      return this.OFFSET_HEIGHT_PX;
    },
    scrollIfAnchor: function (href, pushToHistory) {
      var match, anchorOffset;
      if (!this.ANCHOR_REGEX.test(href)) {
        return false;
      }
      match = document.getElementById(href.slice(1));
      if (match) {
        anchorOffset = $(match).offset().top - this.getFixedOffset();
        $('html, body').animate({ scrollTop: anchorOffset });
        if (HISTORY_SUPPORT && pushToHistory) {
          history.pushState({}, document.title, location.pathname + href);
        }
      }
      return !!match;
    },
    scrollToCurrent: function (e) {
      if (this.scrollIfAnchor(window.location.hash) && e) {
        e.preventDefault();
      }
    },
    delegateAnchors: function (e) {
      var elem = e.target;

      if (this.scrollIfAnchor(elem.getAttribute('href'), true)) {
        e.preventDefault();
      }
    }
  };
  $(document).ready($.proxy(anchorScrolls, 'init'));
})(window.document, window.history, window.location);

/**
 * Scroll to top
 */

var toggleHeight = $(window).outerHeight() / 3;

$(window).scroll(function () {
  if ($(window).scrollTop() > toggleHeight) {
    //Adds active class to make button visible
    $(".top_link").addClass("visible");

  } else {
    //Removes active class to make button visible
    $(".top_link").removeClass("visible");
  }
});

//Scrolls the user to the top of the page again
$(".top_link").click(function () {
  $("html, body").animate({ scrollTop: 0 }, "slow");
  return false;
});

/**
 * Activate tooltips
 */

 $(function () {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl, {
      animation: false
    })
  })
})


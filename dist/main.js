var txt = $.get('https://www.fantasybasketballnerd.com/service/schedule/BOS')

console.log(txt)

// if (window.DOMParser)
//   {
//   parser=new DOMParser();
//   xmlDoc=parser.parseFromString(txt,"text/xml");
//   }
// else // Internet Explorer
//   {
//   xmlDoc=new ActiveXObject("Microsoft.XMLDOM");
//   xmlDoc.async=false;
//   xmlDoc.loadXML(txt);
//   }
//


;(function () {

  $.fn.getSchedule = $.fn.getSchedule || function () {
    var url = $(this).attr('data-url')
    var txt = $.get(url)
    console.log(txt)
  }

  $.fn.findIncludeSelf = function (selector) {
    return this.find(selector).addBack(selector)
  }

  function isFunction (fn) {
    return fn && {}.toString.call(fn) === '[object Function]'
  }

  /**
   * Initialize javascript listeners for all '[data-init]' elements found in $el.
   */
  $.fn.initJS = $.fn.initJS || function () {
    var $el
    $el = $(this)
    $el.findIncludeSelf('[data-init]').each(function () {
      var self, $this, fnames
      self = this
      $this = $(this)
      fnames = $this.attr('data-init').trim().split(/\s+/)
      _.forEach(fnames, function (fname) {
        var fnameParts,
          fn,
          options
        fnameParts = fname.split('.')
        if (fnameParts.length === 1) {
          options = $this.attr('data-options')
          if (options) {
            options = JSON.parse(options)
          }
          if (!isFunction($this[fname])) {
            throw format('$.fn.{0} is not a function', fname)
          }
          $this[fname](options)
        } else {
          fn = $this
          _.forEach(fnameParts, function (fnamePart) {
            fn = fn[fnamePart]
          })
          fn(self)
        }
      })
    })
  }


  $(function () {
    $('body').initJS()
  })

}).call(this)

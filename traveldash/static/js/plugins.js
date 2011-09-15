
// usage: log('inside coolFunc', this, arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  if(this.console) {
    arguments.callee = arguments.callee.caller;
    var newarr = [].slice.call(arguments);
    (typeof console.log === 'object' ? log.apply.call(console.log, console, newarr) : console.log.apply(console, newarr));
  }
};

// make it safe to use console.log always
(function(b){function c(){}for(var d="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,timeStamp,profile,profileEnd,time,timeEnd,trace,warn".split(","),a;a=d.pop();){b[a]=b[a]||c}})((function(){try
{console.log();return window.console;}catch(err){return window.console={};}})());


// place any jQuery/helper plugins in here, instead of separate, slower script files.

/**
 * Create tooltips on click (for supporting touch interfaces).
 * Original Author: C. Scott Asbach
 */
$.touchTooltip = function() {
    if (!Modernizr.touch) {
        // do normal JS events if we're not on a touch device
        return;
    }

	/**
	 * store the value of and then remove the title attributes from the
	 * abbreviations (thus removing the default tooltip functionality of
     * the abbreviations)
	 */
	$('abbr[title]').each(function(){		
		$(this).data('title',$(this).attr('title'));
		$(this).removeAttr('title');
	})

	/**
	 * when abbreviations are clicked trigger their mouseover event then fade the tooltip
	 * (this is friendly to touch interfaces)
	 */
	.click(function(){
		// first remove all existing abbreviation tooltips
		$('abbr').next('.tooltip').remove();

		// create the tooltip
		$(this).after('<span class="tooltip">' + $(this).data('title') + '</span>');

		// position the tooltip 4 pixels above and 4 pixels to the left of the abbreviation
        var pos = $(this).position();
		$(this).next().css({left:pos.left, top:pos.top});			

		// after a slight 2 second fade, fade out the tooltip for 1 second
		$(this).next().animate({opacity: 0.9},{duration: 2000, complete: function(){
			$(this).fadeOut(800);
		}});
	})
};
$(function() {
  $.touchTooltip();
});

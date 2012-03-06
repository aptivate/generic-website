(function () {
	var subsector = null,
		envelope = $("<div>"),
		// Define selectors and use them everywhere
		sec_selector = "#id_sector",
		subsec_selector = "#id_subsector";

	// Make a copy of subsector that we can use later on
	envelope.html($(subsec_selector).parent().html());
	envelope.find("label").remove();
	subsector = $.trim(envelope.html());

	// You can't hide optgroups/options well in WebKit and IE. Hence you need
	// to clone select and remove parts you don't need.
	$(sec_selector).bind("change", function (e) {
		var index = this.options.selectedIndex,
			group = this.options[index].value
			new_subsector = $("<div>").html(subsector)[0].firstChild,
			$subsector_parent = $(subsec_selector).parent();

		if (group !== "") {
			// Show just selected subsector
			$(new_subsector).find("optgroup").each(function (i, optgrp) {
				if (this.label !== group) {
					$(this).remove();
				}
			});
		}
		$subsector_parent.find("select, optgroup, option").remove(); // Chrome can remove select but leave children
		$(new_subsector).appendTo($subsector_parent);
	}).change(); // Trigger for loading of pre-filled search forms

	// Add loading indicator on search forms
	$("form.search_advanced").bind("submit", function () {
		$('<div class="dialog loading">Loading...</div>')
			.css({
				left: "135%",
				top: "130px",
				display: "block"
			}).appendTo($(".content"));
	});

	// Highlight keywords
	/*
	(function highlightKeywords() {
		var keywords = $(".search_results > h2 span").html(),
			terms_re = {};

		if (keywords) {
			keywords = keywords.split(" ");
			$.each(keywords, function (i, term) { terms_re[term] = new RegExp(term, "i"); });
			$(".search_results .article h2 a, .search_results .article p.findings").each(function (i, el) {
				var $this = $(el),
					txt = $this.html();
				for(term in terms_re) {
					txt = txt.split(terms_re[term]).join('<span class="highlight">'+term+'</span>');
				}
				$this.html(txt);
			});
		}
	})();
	*/
})();

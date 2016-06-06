// requires jqery.js or like (zepto)
var html_ajax_env = function ($containers_group, form_filter, html_changed_handler) {
    // support jquery objects... ==> string selector.
    var container_selector;
    if ($containers_group instanceof jQuery) {
        container_selector = $containers_group.selector;
    }
    else {
        container_selector = $containers_group;
        $containers_group = $(container_selector);
    }
    // if form_filter wasn't provider then it applies to all forms in the container
    if ((typeof html_changed_handler === "undefined") && (typeof form_filter !== "string")) {
        // shift right args - set form filter to default (no filter)
        html_changed_handler = form_filter;
        form_filter = false;
    }
    if (form_filter || false) {
        // we have a filter
    }
    else {
        form_filter = 'form';
    }
    // consts - events
    var form_posted_event = "form_posted";
    var html_changed_event = "html_changed";
    var form_bind_event = "form_bound";

    // This should only happen ONCE! as the container itself does not refresh - only its content.
    if (html_changed_handler) {
        $containers_group.on(html_changed_event, html_changed_handler);
    }

    var my_container = function ($the_form) {
        if (!container_selector) {
            // explicit container given not using selector.
            return $containers_group;
        }
        return $the_form.parents(container_selector).first();
    };

    // on submit - update html.
    // rebind all matching forms in updated container.
    // sending change event for container by searching the parent for all forms received
    var on_ajax_submit = function (event) {
        var $the_form = $(this);
        event.preventDefault();
        // we hooked this method on the form.
        var data = new FormData(this);
        var $container = my_container($the_form);
        var method = $(this).attr('method');
        var processData=false;

        if (method.toUpperCase()=='GET'){
            // form ==> get
            processData=true;
            data = $the_form.serialize();
        }


        $.ajax({
            // bound to ajax.
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: data,
            cache: false,
            processData: processData,
            contentType: false,
            success: function (data) {
                // not notify for used forms.
                $container.trigger(form_posted_event, $the_form);

                $container.html(data);
                var $fresh_forms = bind_form_with_ajax($container);
                $container.trigger(html_changed_event, data);
            }
        });
        return false;
    };

    var bind_form_with_ajax = function () {
        // protect from rebind bounded implicitly
        var $form_objs = $containers_group.find('form').filter(form_filter).filter(':not(.ajaxified)');
        // replace submit event with ajax method.
        $form_objs.on('submit', on_ajax_submit);
        $form_objs.addClass("ajaxified");
        $form_objs.each(function (i) {
            var $that = $(this);
            // notify all/newly bounded by : the form, event, no data - provide the form ==>
            // each form used for parent container.trigger with form_bind_event and the newly ajaxified form
            my_container($that).trigger( form_bind_event, $that);

        });
        return $form_objs;
    };

    return {
        container_selector: container_selector,
        $containers_group: $containers_group,
        form_filter: form_filter,
        html_changed_handler: html_changed_handler,
        html_changed_event: html_changed_event,
        form_bind_event: form_bind_event,
        on_ajax_submit: on_ajax_submit,
        bind_form_with_ajax: bind_form_with_ajax
    };
};

var setup_ajax_on = function ($containers_group, form_filter, html_changed_handler) {
    var e = html_ajax_env($containers_group, form_filter, html_changed_handler);
    var $all_forms = e.bind_form_with_ajax();
};

// do not notify html change.
var setup_ajax_on_url = function (url, $containers_group, form_filter, html_changed_handler) {
    var data = undefined, processData=false;

    if (url instanceof Array) {
        var arr = url;
        url = arr.shift();
        data = arr.shift();
    }
    if (data){processData=true;}
    var e = html_ajax_env($containers_group, form_filter, html_changed_handler);

    e.$containers_group.each(function (i) {
        var $container = $(this);

        $.ajax({
            // do initial ajax.
            url: url,
            type: 'GET',
            data: data,
            cache: false,
            processData: processData,
            contentType: false,
            success: function (data) {
                $container.html(data);
                var $all_forms = e.bind_form_with_ajax();
            }
        });
    });
    return false;
};

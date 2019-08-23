function main(splash)
    local num_scrolls = 10
    local scroll_delay = 1.0

    -- ================================================
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)

    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end
    -- ================================================

    
    splash:set_viewport_full()

    return {
        html = splash:html(),
        png = splash:png(),
    }
end
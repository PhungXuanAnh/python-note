function main(splash)
    -- local url = "https://m.facebook.com/officialdoda/"
    local url = splash.args.url

    splash:init_cookies(splash.args.cookies)
    assert(splash:go(url))
    assert(splash:wait(3))

    -- =================================================
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    for _ = 1, 3 do
        scroll_to(0, get_body_height())
        splash:wait(3)
    end

    -- =================================================
    -- splash:set_viewport_full()
    
    return {
        cookies = splash:get_cookies(),
        png = splash:png(),
        html = splash:html(),
    }
end
function main(splash)
    local url = "https://m.facebook.com"
    -- local url = splash.args.url
    local email = "test1.phungxuananh@gmail.com"
    local password = "1234%^&*"


    assert(splash:go(url))
    assert(splash:wait(3))

    local search_input = splash:select('input[name=email]')   
    search_input:send_text(email)
    assert(splash:wait(1))
    
    local search_input = splash:select('input[name=pass]')
    search_input:send_text(password)
    assert(splash:wait(1))
    
    local submit_button = splash:select('button[name=login]')
    submit_button:click()
    assert(splash:wait(3))

    -- =================================================
    local url = "https://m.facebook.com/officialdoda/"
    assert(splash:go(url))
    assert(splash:wait(3))


    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    for _ = 1, 3 do
        scroll_to(0, get_body_height())
        splash:wait(3)
    end
    -- =================================================    

    splash:set_viewport_full()

    return {
        cookies = splash:get_cookies(),
        html = splash:html(),
        png = splash:png(),
    }
end
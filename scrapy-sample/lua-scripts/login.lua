function main(splash)
    local url = "https://www.facebook.com/"
    local email = "test1.phungxuananh@gmail.com"
    local password = "1234%^&*"
    
    -- local url = splash.args.url

    assert(splash:go(url))
    assert(splash:wait(3))

    local search_input = splash:select('input[name=email]')   
    search_input:send_text(email)
    assert(splash:wait(1))
    
    local search_input = splash:select('input[name=pass]')
    search_input:send_text(password)
    assert(splash:wait(1))
    
    -- local submit_button = splash:select('input[class^=primary-btn]')
    local submit_button = splash:select('label[id="loginbutton"] input[type="submit"]')
    assert(splash:wait(1))
    submit_button:click()

    assert(splash:wait(3))

    splash:set_viewport_full()

    return {
        cookies = splash:get_cookies(),
        html = splash:html(),
        png = splash:png(),
    }
end
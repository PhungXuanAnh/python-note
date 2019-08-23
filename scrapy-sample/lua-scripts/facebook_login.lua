function main(splash)
    -- local url = "https://m.facebook.com"
    local url = splash.args.url
    local email = "test1.phungxuananh@gmail.com"
    local password = "1234%^&*"

    -- splash:init_cookies(splash.args.cookies)

    assert(splash:go(url))
    assert(splash:wait(3))

    local search_input = splash:select('input[name=email]')   
    search_input:send_text(email)
    assert(splash:wait(1))
    
    local search_input = splash:select('input[name=pass]')
    search_input:send_text(password)
    assert(splash:wait(1))
    
    -- local submit_button = splash:select('label[id="loginbutton"] input[type="submit"]')
    local submit_button = splash:select('button[name=login]')
    submit_button:click()
    assert(splash:wait(3))

    -- local submit_button = splash:select('button[value=OK]')
    -- local submit_button = splash:select('a[role=button]')
    -- submit_button:click()
    -- url = "https://m.facebook.com/officialdoda/"
    -- assert(splash:go(url))
    -- assert(splash:wait(3))

    
    -- =================================================
    -- local url = "https://www.facebook.com/officialdoda/"
    -- assert(splash:go(url))
    -- assert(splash:wait(3))


    -- local scroll_to = splash:jsfunc("window.scrollTo")
    -- local get_body_height = splash:jsfunc(
    --     "function() {return document.body.scrollHeight;}"
    -- )
    -- scroll_to(0, get_body_height())
    -- assert(splash:wait(3))

    -- =================================================    

    -- splash:set_viewport_full()

    return {
        cookies = splash:get_cookies(),
        html = splash:html(),
        png = splash:png(),
    }
end
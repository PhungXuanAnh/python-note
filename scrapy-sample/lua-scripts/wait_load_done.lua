-- use splash:wait() in a loop and check for availability of some element 
-- (like footer)

function main(splash)
    assert(splash:autoload("https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"))
    assert(splash:go(splash.args.url))

    local js = [[
        var $j = jQuery.noConflict();
        $j('#USER').val('frankcastle');
        $j('#password').val('punisher');
        $j('.button-oblong-orange.button-orange a').click();
        $j('body').empty() // clear body, otherwise the wait_for footer will always be true
    ]]

    assert(splash:runjs(js))

    function wait_for(splash, condition)
        while not condition() do
            splash:wait(0.05)
        end
    end

    wait_for(splash, function()
        return splash:evaljs("document.querySelector('#footer') != null")
    end)

    return {
        html = splash:html()
    }
end
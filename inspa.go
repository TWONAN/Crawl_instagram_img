package main

import (
	"fmt"
	"github.com/gocolly/colly"
	"github.com/gocolly/colly/proxy"
)
func main(){
	// Instantiate default collector
	c := colly.NewCollector()
	if p,err := proxy.RoundRobinProxySwitcher(
		"socks5://127.0.0.1:1080",
	);err == nil {
        c.SetProxyFunc(p)
    }
	c.UserAgent="Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
	// On every a element which has href attribute call callback
	c.OnHTML("body", func(e *colly.HTMLElement) {
		link := e.Text
		// Print link
		fmt.Println(link)
		// Visit link found on page
		// Only those links are visited which are in AllowedDomains
		// c.Visit(e.Request.AbsoluteURL(link))
	})

	// Before making a request print "Visiting ..."
	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL.String())
		fmt.Printf("UA:%s",r.Headers)
	})

	// Start scraping on https://hackerspaces.org
	c.Visit("https://www.instagram.com/nanaouyang/")
}

<p align="center"><img src="docs/assets/banner.svg" alt="Inzomio: online bookings for independent professionals" width="100%"></p>

<p align="center">
  <a href="https://inzomio.app"><img alt="Website" src="https://img.shields.io/badge/inzomio.app-live-fab200"></a>
  <a href="https://youtu.be/acQ1y2dnfbo"><img alt="Demo video" src="https://img.shields.io/badge/YouTube-demo-0a0a0a?logo=youtube"></a>
  <a href="https://www.instagram.com/inzomio.app/"><img alt="Instagram" src="https://img.shields.io/badge/Instagram-@inzomio.app-0a0a0a?logo=instagram"></a>
  <a href="https://www.linkedin.com/company/145218836/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Inzomio-0a0a0a"></a>
  <img alt="Stack" src="https://img.shields.io/badge/Next.js_·_Supabase_·_Vercel-0a0a0a">
  <img alt="AI" src="https://img.shields.io/badge/AI_agent-Claude_Haiku_4.5-fab200">
</p>

# Inzomio

> Online bookings for independent professionals: own website, a link in bio, bookings that confirm themselves and an AI agent that answers clients 24/7.

This repository is a **portfolio showcase**. It tells the story, the product and the architecture of Inzomio. The source code and database live in a private repository: there's no business logic, credentials or schemas here.

| | |
|---|---|
| **Problem** | Nutritionists, psychologists, physiotherapists, beauty and wellness professionals coordinate bookings by message, one by one. |
| **Solution** | Every business gets its own page, an agenda that confirms bookings on its own, a management panel and an AI agent. |
| **Business model** | Free $0 · Profesional $14.900 · Empresas $24.900 per month (ARS). 15-day trial, no fee per booking. |
| **Build** | Started as a weekend experiment with Claude Code; today a product in production. |
| **Status** | In production at [inzomio.app](https://inzomio.app). Public launch on Instagram, LinkedIn and YouTube in September 2026. |

**Contents:** [Demo](#see-it-in-90-seconds) · [Product](#the-product) · [AI agent](#the-ai-agent) · [Screens](#real-screens) · [Plans](#plans) · [Channels](#communication-channels) · [Architecture](#architecture) · [Origin](#origin-and-method) · [Roadmap](#roadmap)

---

## See it in 90 seconds

<p align="center">
  <a href="https://youtu.be/acQ1y2dnfbo"><img src="https://img.youtube.com/vi/acQ1y2dnfbo/maxresdefault.jpg" alt="Watch the Inzomio demo on YouTube" width="80%"></a>
</p>
<p align="center"><b><a href="https://youtu.be/acQ1y2dnfbo">▶ Inzomio: online bookings for independent professionals · full demo</a></b></p>

## The product

<p align="center"><img src="docs/assets/modules.svg" alt="Own website, bookings, Inzomio Link, AI agent, admin panel" width="100%"></p>

One codebase serves four surfaces:

| Surface | For | What it does |
|---|---|---|
| Marketing site | Prospects | Problem, how it works, real pricing and sign-up |
| Business page | Each business's clients | Its own website (paid plans) or Inzomio Link (Free), with booking and the agent |
| Business panel | The business owner | Bookings, clients, services, page builder, agent, subscription |
| Platform panel | The Inzomio team | Plans, features per plan, agent engine and support |

Bookings are validated on the server, not only on screen, and the public pages are protected against bots and abuse.

## The AI agent

The agent is the core differentiator. There are **two**, each with its own job.

<p align="center"><img src="docs/assets/agent.svg" alt="Client agent and internal agent" width="100%"></p>

**Client agent: on every public page.** It answers what a visitor asks about services (price, duration, deposit), policies and aftercare, searching the knowledge base the business loaded. In the chat it shows shortcut cards (see services, book).
- It **doesn't book by itself**: when someone wants to book, change or cancel, it hands off to the booking page or the business's WhatsApp. It's a design decision so the AI can't make booking mistakes.
- **Free / Profesional:** a matcher over hand-loaded FAQs, with no AI and no API cost.
- **Empresas:** a real conversational agent running Claude Haiku 4.5, or TypeSafe (Jev), chosen per business from the platform panel.
- Usage limits keep AI cost under control.

**Internal agent: inside the admin panel.** It answers the owner about their own business with real data: bookings for a day or a range, unconfirmed bookings, pending balances, client search (with a direct WhatsApp link), a general summary, services and profile.
- **Voice dictation** to talk instead of type.
- When it can't do something yet, **"Propose this improvement"** sends the idea as a ticket to the Inzomio team. The product learns from its own users.

<table>
  <tr>
    <td width="33%"><img src="docs/screenshots/mobile-home-agent.jpg" alt="Agent suggestions on mobile"></td>
    <td width="33%"><img src="docs/screenshots/mobile-agent-answer.jpg" alt="Agent answering with a booking card"></td>
    <td width="33%"><img src="docs/screenshots/subscriber-agent-mobile.jpg" alt="Agent on a subscriber's page"></td>
  </tr>
  <tr>
    <td align="center"><sub>Suggested questions</sub></td>
    <td align="center"><sub>Answer with a booking shortcut</sub></td>
    <td align="center"><sub>Same agent on a client's business</sub></td>
  </tr>
</table>

## Real screens

### Marketing site and pricing · `inzomio.app`

<table>
  <tr>
    <td width="50%"><img src="docs/screenshots/marketing-landing.jpg" alt="Inzomio marketing landing"></td>
    <td width="50%"><img src="docs/screenshots/pricing.jpg" alt="Pricing page with Free, Profesional and Empresas"></td>
  </tr>
</table>

### Subscriber website · demo business "Spa Serenity"

Each business gets its own page with its own colors, services, gallery and map. This is the demo business on desktop:

<p align="center"><img src="docs/screenshots/subscriber-landing-desktop.jpg" alt="Subscriber landing page on desktop" width="100%"></p>

<table>
  <tr>
    <td width="50%"><img src="docs/screenshots/subscriber-booking-desktop.jpg" alt="Booking calendar on desktop"></td>
    <td width="50%"><img src="docs/screenshots/subscriber-agent-desktop.jpg" alt="Agent on desktop"></td>
  </tr>
  <tr>
    <td align="center"><sub>Booking: real availability against the agenda</sub></td>
    <td align="center"><sub>The business agent on desktop</sub></td>
  </tr>
</table>

### Mobile first: booking flow and Inzomio Link

<table>
  <tr>
    <td width="20%"><img src="docs/screenshots/subscriber-landing-mobile.jpg" alt="Subscriber page on mobile"></td>
    <td width="20%"><img src="docs/screenshots/booking-service.jpg" alt="Pick a service"></td>
    <td width="20%"><img src="docs/screenshots/subscriber-calendar-mobile.jpg" alt="Pick a day and time"></td>
    <td width="20%"><img src="docs/screenshots/subscriber-form-mobile.jpg" alt="Client details"></td>
    <td width="20%"><img src="docs/screenshots/subscriber-link-mobile.jpg" alt="Inzomio Link of a business"></td>
  </tr>
  <tr>
    <td align="center"><sub>Business page</sub></td>
    <td align="center"><sub>1 · Service</sub></td>
    <td align="center"><sub>2 · Day and time</sub></td>
    <td align="center"><sub>3 · Details</sub></td>
    <td align="center"><sub>Inzomio Link</sub></td>
  </tr>
</table>

<p align="center"><img src="docs/screenshots/inzomio-link.jpg" alt="Inzomio's own Inzomio Link" width="260"><br><sub>Inzomio's own link in bio, built with Inzomio Link</sub></p>

### Admin panel

Home with KPIs (bookings, clients, revenue, services) and today's bookings, calendar and bookings table, services, clients with history, Inzomio Link editor, visual page builder with live preview, agent setup and subscription. Everything works on mobile.

> 📸 Admin panel screenshots: pending. They're added once they're captured from a demo account.

## Plans

<p align="center"><img src="docs/assets/plans.svg" alt="Free, Profesional and Empresas plans" width="100%"></p>

Plans and features aren't hard-coded: a central registry in the platform panel decides, feature by feature, which plan includes it, with per-business exceptions. If a trial ends without a paid plan, the account moves to Free automatically: the page and data stay.

## Communication channels

| Channel | Use |
|---|---|
| [inzomio.app](https://inzomio.app) | Marketing site, pricing and sign-up |
| [Instagram · @inzomio.app](https://www.instagram.com/inzomio.app/) | Posts, carousels, reels and stories for professionals |
| [LinkedIn](https://www.linkedin.com/company/145218836/) | Company page, B2B and partnerships |
| [YouTube · @Inzomio-app](https://www.youtube.com/@Inzomio-app) | Full demo and step-by-step tutorials |
| Email · inzomio.app@gmail.com | Support and contact |

### YouTube: "Your first steps in Inzomio"

A tutorial series so each business can set up its account alone. Thumbnails made with the brand generator:

<table>
  <tr>
    <td><img src="docs/youtube/yt-tutorial-01-primeros-pasos.jpg" alt="Tutorial 1: first steps"></td>
    <td><img src="docs/youtube/yt-tutorial-02-servicios.jpg" alt="Tutorial 2: services"></td>
    <td><img src="docs/youtube/yt-tutorial-03-horarios-y-bloqueos.jpg" alt="Tutorial 3: hours and blocks"></td>
  </tr>
  <tr>
    <td><img src="docs/youtube/yt-tutorial-04-turnos.jpg" alt="Tutorial 4: bookings"></td>
    <td><img src="docs/youtube/yt-tutorial-05-google-calendar.jpg" alt="Tutorial 5: Google Calendar"></td>
    <td><img src="docs/youtube/yt-tutorial-06-inzomio-link.jpg" alt="Tutorial 6: Inzomio Link"></td>
  </tr>
  <tr>
    <td><img src="docs/youtube/yt-tutorial-07-tu-pagina.jpg" alt="Tutorial 7: your website"></td>
    <td><img src="docs/youtube/yt-tutorial-08-agente-ia.jpg" alt="Tutorial 8: AI agent"></td>
    <td><img src="docs/youtube/yt-tutorial-09-clientes.jpg" alt="Tutorial 9: clients"></td>
  </tr>
  <tr>
    <td><img src="docs/youtube/yt-tutorial-10-cuenta-y-plan.jpg" alt="Tutorial 10: account and plan"></td>
    <td><img src="docs/youtube/yt-tutorial-escalonados.jpg" alt="Extra: staggered bookings"></td>
    <td></td>
  </tr>
</table>

## Architecture

<p align="center"><img src="docs/assets/architecture.svg" alt="Architecture diagram" width="100%"></p>

- **Real multi-tenancy:** every business has its own page and booking flow, isolated with Row Level Security in Supabase. One codebase serves all of them.
- **Three permission levels:** visitor, business owner and platform team.
- **Built-in page builder:** editing the landing page lives inside the product, with live preview.
- **Payments:** subscriptions charged with Mercado Pago. Clients pay the business by transfer or cash, with no fee per booking.

**Stack:** Next.js (App Router) · React · TypeScript · Supabase (Postgres, Auth, RLS) · Vercel · Claude Haiku 4.5 and TypeSafe for the agents · Mercado Pago · Google Calendar · bot protection.

## Origin and method

Inzomio started as an experiment: how far could a real product go working side by side with an AI agent (Claude Code), without writing code by hand. The working name was *Insomnio*, literally, because it started on a Friday at dawn and ran through a whole weekend of conversation with the agent. The brand later became **Inzomio**.

It was also a test of **method**: whether a product management process could hold a build at that speed. It started as an MVP and grew, with the same loop at every stage, into the product in production it is today:

<p align="center"><img src="docs/assets/process.svg" alt="Spot, understand, hypothesize, iterate, production" width="100%"></p>

## Roadmap

<p align="center"><img src="docs/assets/roadmap.svg" alt="Roadmap" width="100%"></p>

The main growth channel is agreements with professional associations (Mendoza first), with direct outreach, creators and an affiliate program as support. Next on the product: multiple agendas or professionals per business and card or Mercado Pago payments at booking.

---

<p align="center"><img src="docs/brand/inzomio-symbol.svg" alt="Inzomio symbol" width="56"></p>
<p align="center">
  <a href="https://inzomio.app"><b>inzomio.app</b></a> ·
  <a href="https://youtu.be/acQ1y2dnfbo">Demo</a> ·
  <a href="https://www.youtube.com/@Inzomio-app">YouTube</a> ·
  <a href="https://www.instagram.com/inzomio.app/">Instagram</a> ·
  <a href="https://www.linkedin.com/company/145218836/">LinkedIn</a>
</p>
<p align="center">Built by Jonathan Godoy · <a href="https://jonathangodoy.xyz/en"><b>jonathangodoy.xyz</b></a></p>

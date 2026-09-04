# Architecture

`browser → FastAPI domain endpoints → Trestle HTTP API → configured Trestle store`

Pydantic validates the complete observation shape before a fixed collection route is called. The Trestle service token never enters generated HTML or browser responses. Static presentation remains independently rebuildable with Nift.

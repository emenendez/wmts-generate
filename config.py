wmts = {
	'Title': 'My WMTS Service',  # Title of this WMTS service
	'WMTS_Base_Directory': 'http://wmts.example.com/',  # URL of this WMTS service, with trailing slash
	'Layers':
	[
		{
			'Title': 'Example Layer',  # Layer name
			'Identifier': 'example',  # Unique identifier
			'Format': 'image/png',  # Tile format
			'URL_Template': 'http://wmts.example.com/example/{TileMatrix}/{TileCol}/{TileRow}.png',  # Template to fetch tiles
		},
	]
}
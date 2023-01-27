project = 'Doc Tests'
copyright = '2023 Jessica L. Hamilton'
author = 'Jessica L. Hamilton'

version = '0.1'
release = '0.1'

extensions = [
	'myst_parser',
]

myst_enable_extensions = [
	'colon_fence',
	'deflist',
	'substitution',
]

templates_path = ['_templates']

sources_suffix = '.rst'

master_doc = 'index'

language = 'en'

exclude_patterns = ['_build']

pygments_style = None

html_theme = 'haiku'

html_static_path = ['_static']

smartquotes = True

def setup(app):
	from docutils import nodes
	from docutils.nodes import Element, Node, Text
	from docutils.parsers.rst import Directive, directives

	from sphinx.application import Sphinx
	from sphinx.environment import BuildEnvironment
	from sphinx.writers.html5 import HTML5Translator
	from sphinx.builders import Builder
	from sphinx.util import logging

	from sphinx.builders.html import StandaloneHTMLBuilder

	logger = logging.getLogger(__name__)

	class SectionDirective(Directive):
		has_content = True
		required_arguments = 0

		def run(self):
			return []

	class CustomBuilder(StandaloneHTMLBuilder):
		def __init__(self, app: Sphinx, env: BuildEnvironment = None) -> None:
			super().__init__(app, env)
		
		@property
		def default_translator_class(self):
			return CustomHTMLTranslator
	
	class CustomHTMLTranslator(HTML5Translator):
		def __init__(self, document: nodes.document, builder: Builder) -> None:
			super().__init__(document, builder)

			self.signature_node = None
			self.signature_names = []
		
		# The overarching goal is to be able to collect the descriptions,
		# and store them in the context, then later generate the actual
		# needed HTML at the end...
		
		def visit_desc(self, node: Element) -> None:
			return
		
		def depart_desc(self, node: Element) -> None:
			return
		
		def visit_desc_signature(self, node: Element) -> None:
			self.signature_node = node
		
		def depart_desc_signature(self, node: Element) -> None:
			self.signature_node = None
		
		def visit_desc_signature_line(self, node: Element) -> None:
			return
		
		# Okay, this is mostly working... however, we're terminating
		# too early... this is where the new nodes are needed to
		# delineate an API section, and write the HTML there instead...
		def depart_desc_signature_line(self, node: Element) -> None:
			return
		
		def visit_desc_name(self, node: Element) -> None:
			self.signature_names.append(node)
		
		def depart_desc_name(self, node: Element) -> None:
			return
		
		def visit_section(self, node: Element) -> None:
			logger.warn('start section')
		
		def depart_section(self, node: Element) -> None:
			logger.warn('end section')
			#self.body.append(self.starttag(self.signature_node, 'h3'))
			# we don't have the IDs here...
			self.body.append(self.starttag(node, 'h3'))
			
			# this is where we should be able to collect all the
			# names and generate a single header
			names = []
			for child in self.signature_names:
				names.append(''.join(str(c) for c in child[0].children))
			self.body.append(', '.join(names))

			self.signature_names = []
			self.body.append('</h3>\n\n')

	app.add_directive('section', SectionDirective)
	app.set_translator('html', CustomHTMLTranslator, True)

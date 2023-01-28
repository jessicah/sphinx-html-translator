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

import sys, os

sys.path.append(os.path.abspath('.'))

from docutils.nodes import Element, Node, Text

from custom import startsection, endsection, abigroup

def setup(app):
	from docutils import nodes
	from docutils.parsers.rst import Directive, directives

	from sphinx.application import Sphinx
	from sphinx.environment import BuildEnvironment
	from sphinx.writers.html5 import HTML5Translator
	from sphinx.builders import Builder
	from sphinx.util import logging

	from sphinx.builders.html import StandaloneHTMLBuilder

	logger = logging.getLogger(__name__)

	class AbiGroupDirective(Directive):
		has_content = True
		required_arguments = 0

		def run(self):
			text = '\n'.join(self.content)
			node = abigroup(text)
			self.add_name(node)
			self.state.nested_parse(self.content, self.content_offset, node)
			return [node]

	class CustomBuilder(StandaloneHTMLBuilder):
		def __init__(self, app: Sphinx, env: BuildEnvironment = None) -> None:
			super().__init__(app, env)
		
		@property
		def default_translator_class(self):
			return CustomHTMLTranslator
	
	class CustomHTMLTranslator(HTML5Translator):
		def __init__(self, document: nodes.document, builder: Builder) -> None:
			super().__init__(document, builder)

			self.signature_ids = []
			self.signature_names = []

		# The overarching goal is to be able to collect the descriptions,
		# and store them in the context, then later generate the actual
		# needed HTML at the end...

		def visit_desc(self, node: Element) -> None:
			return
		
		def depart_desc(self, node: Element) -> None:
			return
		
		def visit_desc_signature(self, node: Element) -> None:
			self.signature_ids += node.attributes['ids']
		
		def depart_desc_signature(self, node: Element) -> None:
			return
		
		def visit_desc_signature_line(self, node: Element) -> None:
			return
		
		def depart_desc_signature_line(self, node: Element) -> None:
			# we still want to capture the entire signature line,
			# and generate similar HTML as the original HTMLTranslator
			return
		
		def visit_desc_name(self, node: Element) -> None:
			logger.warn('desc_name')
			self.signature_names.append(node)
			logger.warn(self.signature_names)
		
		def depart_desc_name(self, node: Element) -> None:
			return
		
		def visit_section(self, node):
			logger.warn('section')
		
		def depart_section(self, node):
			logger.warn('leave section')
		
		def visit_startsection(self, node: Element) -> None:
			logger.warn('start section')
			logger.warn(self.signature_names)
			self.signature_names = []
		
		def depart_startsection(self, node: Element) -> None:
			logger.warning('depart start section')
		
		def visit_endsection(self, node: Element) -> None:
			logger.warning('visit end section')
		
		def depart_endsection(self, node: Element) -> None:
			logger.warn('end section')
		
		def visit_abigroup(self, node):
			self.signature_names = []
			self.current_body = self.body
			self.body = []
		
		def depart_abigroup(self, node):
			logger.warn('depart abigroup')
			# this isn't quite what we want... we want to grab
			# the IDs from the `desc_signature`
			node.attributes['ids'] = self.signature_ids
			self.signature_ids = []
			text = self.starttag(node, 'h3')
			
			names = []
			for child in self.signature_names:
				names.append(''.join(str(c) for c in child[0].children))
			text += ', '.join(names)
			logger.warn(', '.join(names))
			text += '</h3>\n\n'

			self.body = self.current_body + [text] + self.body

			self.signature_names = []

	app.add_directive('abi-group', AbiGroupDirective)
	app.set_translator('html', CustomHTMLTranslator, True)

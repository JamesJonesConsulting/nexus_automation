import xml.etree.ElementTree as ET
import os
from sys import argv

namespace = "http://karaf.apache.org/xmlns/features/v1.6.0"
xmlfile = argv[1]

ET.register_namespace("", namespace)

tree = ET.parse(xmlfile)
root = tree.getroot()
elm = root.find(".//{%s}feature[@name='nexus-core-feature']/{%s}feature[@prerequisite='true']" % (namespace, namespace))
print(elm)
core_feature = root.find(".//{%s}feature[@name='nexus-core-feature']" % (namespace,))
print(core_feature)
cpan_feature = ET.SubElement(core_feature, "{%s}feature" % (namespace,), attrib={
	"prerequisite": "false",
	"dependency": "false"
})
cpan_feature.text = "nexus-repository-cpan"
cpan_plugin_root = argv[2]
for path, subdirs, files in os.walk(cpan_plugin_root):
	if len(subdirs) > 0:
		cpan_version = subdirs[0]
		print(cpan_version)

composer_feature = ET.SubElement(core_feature, "{%s}feature" % (namespace,), attrib={
	"prerequisite": "false",
	"dependency": "false"
})
composer_feature.text = "nexus-repository-composer"
composer_plugin_root = argv[3]
for path, subdirs, files in os.walk(composer_plugin_root):
	if len(subdirs) > 0:
		composer_version = subdirs[0]
		print(composer_version)

cpan_full_feature = ET.SubElement(root, "{%s}feature" % (namespace,), attrib={
	"name": "nexus-repository-cpan",
	"description": "org.sonatype.nexus.plugins:nexus-repository-cpan",
	"version": "%s" % cpan_version
})

composer_full_feature = ET.SubElement(root, "{%s}feature" % (namespace,), attrib={
	"name": "nexus-repository-composer",
	"description": "org.sonatype.nexus.plugins:nexus-repository-composer",
	"version": "%s" % composer_version
})

cpan_details = ET.SubElement(cpan_full_feature, "{%s}details" % (namespace,))
cpan_details.text = "org.sonatype.nexus.plugins:nexus-repository-cpan"
cpan_bundles = ET.SubElement(cpan_full_feature, "{%s}bundle" % (namespace,))
cpan_bundles.text = "mvn:org.sonatype.nexus.plugins/nexus-repository-cpan/%s" % (cpan_version,)

composer_details = ET.SubElement(composer_full_feature, "{%s}details" % (namespace,))
composer_details.text = "org.sonatype.nexus.plugins:nexus-repository-composer"
composer_bundles = ET.SubElement(composer_full_feature, "{%s}bundle" % (namespace,))
composer_bundles.text = "mvn:org.sonatype.nexus.plugins/nexus-repository-composer/%s" % (composer_version,)

# ET.indent(tree, space="\t", level=0)
tree.write(xmlfile, encoding="UTF-8", xml_declaration=True)
with open(xmlfile) as f:
	lines = f.readlines()
	lines[0] = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

with open(xmlfile, "w") as f:
	f.writelines(lines)


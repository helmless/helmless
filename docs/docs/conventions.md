# Conventions

This section explains several conventions used in the chart schema documentation.

## Symbols

This documentation use some symbols for illustration purposes. Before you read
on, please make sure you've made yourself familiar with the following list of
conventions:


### <!-- md:version --> – Version { data-toc-label="Version" }

The tag symbol in conjunction with a version number denotes when a specific
feature or behavior was added. Make sure you're at least on this version
if you want to use it.

### <!-- md:default --> – Default value { #default data-toc-label="Default value" }

Some properties in the schemas have default values. The default value of the property is always included.

#### <!-- md:default computed --> – Default value is computed { #default data-toc-label="is computed" }

Some default values are not set to static values but computed from other values.

#### <!-- md:default none --> – Default value is empty { #default data-toc-label="is empty" }

Some properties do not contain default values. This means that the functionality
that is associated with them is not available unless explicitly enabled.

### <!-- md:feature --> – Optional feature { #feature data-toc-label="Optional feature" }

Some features are optional and must be explicitly enabled by setting the property.

### <!-- md:flag experimental --> – Experimental { data-toc-label="Experimental" }

Some newer features are still considered experimental, which means they might
(although rarely) change at any time, including their complete removal.

### <!-- md:flag required --> – Required value { #required data-toc-label="Required value" }

Some properties are required, which means they must be explicitly set in the `values.yaml`.

### <!-- md:type --> – Type { #type data-toc-label="Type" }

All properties have a type, for example `string`, `boolean`, `object`, etc.

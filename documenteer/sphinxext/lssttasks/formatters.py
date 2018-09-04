"""Docutils formatters for different Task and Task configuration objects.
"""

__all__ = (
    'get_field_formatter', 'format_field_nodes',
    'format_configurablefield_nodes', 'format_listfield_nodes',
    'format_choicefield_nodes', 'format_rangefield_nodes',
    'create_dtype_item_node',
    'create_field_type_item_node', 'create_default_item_node',
    'create_default_target_item_node', 'create_description_node'
)

from docutils import nodes

from ..utils import parse_rst_content, make_python_xref_nodes, make_section
from .taskutils import typestring


def get_field_formatter(field):
    """Get the config docutils node formatter function for document a config
    field.

    Parameters
    ----------
    field : ``lsst.pex.config.field.Field``
        Config field.

    Returns
    -------
    formatter : callable
        A docutils node formatter corresponding to the ``field``. Formatters
        take positional arguments:

        field_name (`str`)
            Name of the configuration field (the attribute name of on the
            config class).
        field (``lsst.pex.config.Field``)
            A configuration field.
        section_id (`str`)
            Unique identifier for this field. This is used as the id and name
            of the section node.
        state (``docutils.statemachine.State``)
            Usually the directive's ``state`` attribute.

    Raises
    ------
    ValueError
        Raised if the field type is unknown.
    """
    try:
        return FIELD_FORMATTERS[typestring(field)]
    except KeyError:
        raise ValueError('Unknown field type {0!r}'.format(field))


def format_field_nodes(field_name, field, section_id, state):
    """Create a section node that documents a Field config field.

    Parameters
    ----------
    field_name : `str`
        Name of the configuration field (the attribute name of on the config
        class).
    field : ``lsst.pex.config.Field``
        A configuration field.
    section_id : `str`
        Unique identifier for this field. This is used as the id and name of
        the section node.
    state : ``docutils.statemachine.State``
        Usually the directive's ``state`` attribute.

    Returns
    -------
    ``docutils.nodes.section``
        Section containing documentation nodes for the Field.
    """
    from lsst.pex.config import Field
    if not isinstance(field, Field):
        message = ('Field {0} ({1!r}) is not an '
                   'lsst.pex.config.Field type. It is an {2!s}.')
        raise ValueError(message.format(field_name, field, type(field)))

    # Title is the field's attribute name
    title = nodes.title(text=field_name)

    dl = nodes.definition_list()
    dl += create_default_item_node(field, state)
    dl += create_dtype_item_node(field, state)
    dl += create_field_type_item_node(field, state)

    # Doc for this ConfigurableField, parsed as rst
    desc_node = create_description_node(field, state)

    # Package all the nodes into a `section`
    section = make_section(
        section_id=section_id,
        contents=[title, dl, desc_node])

    return section


def format_configurablefield_nodes(field_name, field, section_id, state):
    """Create a section node that documents a ConfigurableField config field.

    Parameters
    ----------
    field_name : `str`
        Name of the configuration field (the attribute name of on the config
        class).
    field : ``lsst.pex.config.ConfigurableField``
        A configuration field.
    section_id : `str`
        Unique identifier for this field. This is used as the id and name of
        the section node.
    state : ``docutils.statemachine.State``
        Usually the directive's ``state`` attribute.

    Returns
    -------
    ``docutils.nodes.section``
        Section containing documentation nodes for the ConfigurableField.
    """
    from lsst.pex.config import ConfigurableField
    if not isinstance(field, ConfigurableField):
        message = ('Field {0} ({1!r}) is not an '
                   'lsst.pex.config.ConfigurableField type. It is an {2!s}.')
        raise ValueError(message.format(field_name, field, type(field)))

    # Title is the field's attribute name
    title = nodes.title(text=field_name)

    dl = nodes.definition_list()
    dl += create_default_target_item_node(field, state)
    dl += create_field_type_item_node(field, state)

    # Doc for this ConfigurableField, parsed as rst
    desc_node = create_description_node(field, state)

    # Package all the nodes into a `section`
    section = make_section(
        section_id=section_id,
        contents=[title, dl, desc_node])

    return section


def format_listfield_nodes(field_name, field, section_id, state):
    """Create a section node that documents a ListField config field.

    Parameters
    ----------
    field_name : `str`
        Name of the configuration field (the attribute name of on the config
        class).
    field : ``lsst.pex.config.ListField``
        A configuration field.
    section_id : `str`
        Unique identifier for this field. This is used as the id and name of
        the section node.
    state : ``docutils.statemachine.State``
        Usually the directive's ``state`` attribute.

    Returns
    -------
    ``docutils.nodes.section``
        Section containing documentation nodes for the ListField.
    """
    from lsst.pex.config import ListField
    if not isinstance(field, ListField):
        message = ('Field {0} ({1!r}) is not an '
                   'lsst.pex.config.ListField type. It is an {2!s}.')
        raise ValueError(message.format(field_name, field, type(field)))

    # Title is the field's attribute name
    title = nodes.title(text=field_name)

    dl = nodes.definition_list()
    dl += create_default_item_node(field, state)
    dl += create_dtype_item_node(field, state)
    dl += create_field_type_item_node(field, state)

    # Doc for this ConfigurableField, parsed as rst
    desc_node = create_description_node(field, state)

    # Package all the nodes into a `section`
    section = make_section(
        section_id=section_id,
        contents=[title, dl, desc_node])

    return section


def format_choicefield_nodes(field_name, field, section_id, state):
    """Create a section node that documents a ChoiceField config field.

    Parameters
    ----------
    field_name : `str`
        Name of the configuration field (the attribute name of on the config
        class).
    field : ``lsst.pex.config.ChoiceField``
        A configuration field.
    section_id : `str`
        Unique identifier for this field. This is used as the id and name of
        the section node.
    state : ``docutils.statemachine.State``
        Usually the directive's ``state`` attribute.

    Returns
    -------
    ``docutils.nodes.section``
        Section containing documentation nodes for the ChoiceField.
    """
    from lsst.pex.config import ChoiceField
    if not isinstance(field, ChoiceField):
        message = ('Field {0} ({1!r}) is not an lsst.pex.config.ChoiceField '
                   'type. It is an {2!s}.')
        raise ValueError(message.format(field_name, field, type(field)))

    # Create a definition list for the choices
    choice_dl = nodes.definition_list()
    for choice_value, choice_doc in field.allowed.items():
        item = nodes.definition_list_item()
        item_term = nodes.term()
        item_term += nodes.literal(text=repr(choice_value))
        item += item_term
        item_definition = nodes.definition()
        item_definition.append(nodes.paragraph(text=choice_doc))
        item += item_definition
        choice_dl.append(item)

    choices_node = nodes.definition_list_item()
    choices_node.append(nodes.term(text='Choices'))
    choices_definition = nodes.definition()
    choices_definition.append(choice_dl)
    choices_node.append(choices_definition)

    # Title is the field's attribute name
    title = nodes.title(text=field_name)

    dl = nodes.definition_list()
    dl += create_default_item_node(field, state)
    dl += choices_node
    dl += create_dtype_item_node(field, state)
    dl += create_field_type_item_node(field, state)

    # Doc for this ConfigurableField, parsed as rst
    desc_node = create_description_node(field, state)

    # Package all the nodes into a `section`
    section = make_section(
        section_id=section_id,
        contents=[title, dl, desc_node])

    return section


def format_rangefield_nodes(field_name, field, section_id, state):
    """Create a section node that documents a RangeField config field.

    Parameters
    ----------
    field_name : `str`
        Name of the configuration field (the attribute name of on the config
        class).
    field : ``lsst.pex.config.RangeField``
        A configuration field.
    section_id : `str`
        Unique identifier for this field. This is used as the id and name of
        the section node.
    state : ``docutils.statemachine.State``
        Usually the directive's ``state`` attribute.

    Returns
    -------
    ``docutils.nodes.section``
        Section containing documentation nodes for the RangeField.
    """
    from lsst.pex.config import RangeField
    if not isinstance(field, RangeField):
        message = ('Field {0} ({1!r}) is not an lsst.pex.config.RangeField '
                   'type. It is an {2!s}.')
        raise ValueError(message.format(field_name, field, type(field)))

    # Format definition list item for the range
    range_node = nodes.definition_list_item()
    range_node += nodes.term(text='Range')
    range_node_def = nodes.definition()
    range_node_def += nodes.paragraph(text=field.rangeString)
    range_node += range_node_def

    # Title is the field's attribute name
    title = nodes.title(text=field_name)

    dl = nodes.definition_list()
    dl += create_default_item_node(field, state)
    dl += range_node
    dl += create_dtype_item_node(field, state)
    dl += create_field_type_item_node(field, state)

    # Doc for this field, parsed as rst
    desc_node = create_description_node(field, state)

    # Package all the nodes into a `section`
    section = make_section(
        section_id=section_id,
        contents=[title, dl, desc_node])

    return section


def create_dtype_item_node(field, state):
    """Create a definition list item node that describes a field's dtype.

    Parameters
    ----------
    field : ``lsst.pex.config.Field``
        A configuration field.
    state : ``docutils.statemachine.State``
        Usually the directive's ``state`` attribute.

    Returns
    -------
    ``docutils.nodes.definition_list_item``
        Definition list item that describes a field's data type.
    """
    type_item = nodes.definition_list_item()
    type_item.append(nodes.term(text="Data type"))
    if field.dtype.__module__ == 'builtins':
        field_dtype = field.dtype.__name__
    else:
        field_dtype = '.'.join((field.dtype.__module__,
                                field.dtype.__name__))
    type_item_content = nodes.definition()
    type_item_content += make_python_xref_nodes(
        field_dtype,
        state,
        hide_namespace=False)
    type_item.append(type_item_content)
    return type_item


def create_field_type_item_node(field, state):
    """Create a definition list item node that describes a field's type.

    Parameters
    ----------
    field : ``lsst.pex.config.Field``
        A configuration field.
    state : ``docutils.statemachine.State``
        Usually the directive's ``state`` attribute.

    Returns
    -------
    ``docutils.nodes.definition_list_item``
        Definition list item that describes a field's type.
    """
    type_item = nodes.definition_list_item()
    type_item.append(nodes.term(text="Field type"))
    field_type = typestring(field)
    type_item_content = nodes.definition()
    type_item_content += make_python_xref_nodes(
        field_type,
        state,
        hide_namespace=True)
    type_item.append(type_item_content)
    return type_item


def create_default_item_node(field, state):
    """Create a definition list item node that describes the default value
    of a Field config.

    Parameters
    ----------
    field : ``lsst.pex.config.Field``
        A configuration field.
    state : ``docutils.statemachine.State``
        Usually the directive's ``state`` attribute.

    Returns
    -------
    ``docutils.nodes.definition_list_item``
        Definition list item that describes the default target of a
        ConfigurableField config.
    """
    default_item = nodes.definition_list_item()
    default_item.append(nodes.term(text="Default"))
    default_item_content = nodes.definition()
    default_item_content.append(
        nodes.literal(text=repr(field.default))
    )
    default_item.append(default_item_content)
    return default_item


def create_default_target_item_node(field, state):
    """Create a definition list item node that describes the default target
    of a ConfigurableField config.

    Parameters
    ----------
    field : ``lsst.pex.config.ConfigurableField``
        A configuration field.
    state : ``docutils.statemachine.State``
        Usually the directive's ``state`` attribute.

    Returns
    -------
    ``docutils.nodes.definition_list_item``
        Definition list item that describes the default target of a
        ConfigurableField config.
    """
    default_item = nodes.definition_list_item()
    default_item.append(nodes.term(text="Default"))
    target_type = '.'.join((field.target.__module__,
                            field.target.__name__))
    default_item_content = nodes.definition()
    default_item_content += make_python_xref_nodes(target_type, state)
    default_item.append(default_item_content)
    return default_item


def create_description_node(field, state):
    """Creates docutils nodes for the Field's description, built from the
    field's ``doc`` and ``optional`` attributes.

    Parameters
    ----------
    field : ``lsst.pex.config.Field``
        A configuration field.
    state : ``docutils.statemachine.State``
        Usually the directive's ``state`` attribute.

    Returns
    -------
    ``docutils.nodes.section``
        Section containing nodes for the ``field``\ 's description.
    """
    doc_container_node = nodes.container()
    doc_container_node += parse_rst_content(field.doc, state)

    # Augment documentation paragraph if the field is optional
    if field.optional:
        optional_para = nodes.paragraph(text="Optional.")
        doc_container_node.append(optional_para)

    return doc_container_node


FIELD_FORMATTERS = {
    'lsst.pex.config.configurableField.ConfigurableField':
        format_configurablefield_nodes,
    'lsst.pex.config.config.Field':
        format_field_nodes,
    'lsst.pex.config.listField.ListField':
        format_listfield_nodes,
    'lsst.pex.config.choiceField.ChoiceField':
        format_choicefield_nodes,
    'lsst.pex.config.rangeField.RangeField':
        format_rangefield_nodes,
}

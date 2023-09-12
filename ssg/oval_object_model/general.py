from ..constants import BOOL_TO_STR
from ..xml import ElementTree


# ----- General functions


def required_attribute(_xml_el, _key):
    if _key in _xml_el.attrib:
        return _xml_el.get(_key)
    raise ValueError(
        "%s is required but was not found in:\n%s" % (_key, repr(_xml_el.attrib))
    )


# ----- General Objects


class OVALBaseObject(object):
    def __init__(self, tag):
        self.tag = tag

    def __eq__(self, __value):
        return self.__dict__ == __value.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def get_xml_element(self):
        raise NotImplementedError


class OVALComponent(OVALBaseObject):
    deprecated = False
    notes = None
    version = "0"

    def __init__(self, tag, id_):
        super(OVALComponent, self).__init__(tag)
        self.id_ = id_

    def get_xml_element(self):
        el = ElementTree.Element(self.tag)
        el.set("id", self.id_)
        el.set("version", self.version)
        if self.deprecated:
            el.set("deprecated", BOOL_TO_STR[self.deprecated])
        if self.notes:
            el.append(self.notes.get_xml_element())
        return el


class OVALEntity(OVALComponent):
    comment = ""

    def __init__(self, tag, id_, properties):
        super(OVALEntity, self).__init__(tag, id_)
        self.properties = properties

    def get_xml_element(self, **attributes):
        el = super(OVALEntity, self).get_xml_element()

        for key, value in attributes.items():
            el.set(key, value)

        if self.comment:
            el.set("comment", self.comment)

        for property_ in self.properties:
            el.append(property_.get_xml_element())

        return el


# ----- OVAL Objects


def load_notes(oval_notes_xml_el):
    if oval_notes_xml_el is None:
        return None
    notes = []
    for note_el in oval_notes_xml_el:
        notes.append(note_el.text)
    return Notes(oval_notes_xml_el.tag, note_el.tag, notes)


class ExceptionEmptyNote(Exception):
    pass


class Notes(OVALBaseObject):
    def __init__(self, tag, note_tag, notes):
        super(Notes, self).__init__(tag)
        self.note_tag = note_tag
        if len(notes) == 0:
            raise ExceptionEmptyNote(
                "Element notes should contain at least one element note."
            )
        self.notes = notes

    def get_xml_element(self):
        notes_el = ElementTree.Element(self.tag)
        for note in self.notes:
            note_el = ElementTree.Element(self.note_tag)
            note_el.text = note
            notes_el.append(note_el)
        return notes_el


# -----


def load_oval_entity_property(end_point_property_el):
    data = OVALEntityProperty(end_point_property_el.tag)
    data.attributes = (
        end_point_property_el.attrib if end_point_property_el.attrib else None
    )
    data.text = end_point_property_el.text
    for child_end_point_property_el in end_point_property_el:
        data.add_child_property(load_oval_entity_property(child_end_point_property_el))
    return data


class OVALEntityProperty(OVALBaseObject):
    attributes = None
    text = None

    def __init__(self, tag):
        super(OVALEntityProperty, self).__init__(tag)
        self.properties = []

    def add_child_property(self, property_):
        self.properties.append(property_)

    def get_xml_element(self):
        property_el = ElementTree.Element(self.tag)
        for key, val in self.attributes.items() if self.attributes is not None else {}:
            property_el.set(key, val)

        if self.text is not None:
            property_el.text = self.text

        for child in self.properties:
            property_el.append(child.get_xml_element())

        return property_el

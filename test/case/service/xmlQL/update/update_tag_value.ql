update:
  -
    update: "/Properties/Property"
    field: "Value"
    value: "new_updated_property_1"
    where: "Value[text()='property_value_1']"

  -
    update: "/Properties/Property"
    field: "Value"
    value: "new_updated_property_2"
    where: "Value[text()='property_value_2']"
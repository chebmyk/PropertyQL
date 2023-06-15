delete:
  - delete: "/Properties/Property[@Code = 'SERVICE']"
    element: "Value/@Active"
    where: "Value[text()='property_value_1']"

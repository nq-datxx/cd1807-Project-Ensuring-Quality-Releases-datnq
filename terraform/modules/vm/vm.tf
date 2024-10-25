resource "azurerm_network_interface" "main" {
  name                = "${var.application_type}-nic"
  location            = var.location
  resource_group_name = var.resource_group

  ip_configuration {
    name                          = "internal"
    subnet_id                     = var.subnet_id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = var.public_ip_address_id
  }
}

resource "azurerm_linux_virtual_machine" "main" {
  name                = "${var.application_type}-${var.resource_type}"
  location            = var.location
  resource_group_name = var.resource_group
  size                = "Standard_B1s"
  admin_username      = var.admin_user
  network_interface_ids = [
    azurerm_network_interface.main.id
  ]
  admin_ssh_key {
    username   = var.admin_user
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDTYYW3ueKCrJZNZaItpoMlN0vAIzaxy9raXxT7M1gOpikmVGzrVMaX5yWOHoxUsGPvjMnedzLxY6NnAwwgd2T5/GEJMKc58pfLQUKSye3r4u2f66PjBfmQ58Vz9UpRBtUHeqbpOIi9ik6kcoU5O+/Q7/yr3NdsQyTcaarWkNcFn2RhqmrmWN28wue4v7ZTI4MUYsD3O2dcGCzQ2vfa1UZZxT7TsONgQ4rbCntx+W1yqivyboHXzQuYJhpQ7RqiVjoJ8K+styvaJGNfyaANx/UUos+YowR+IDwxv8hoT7mNF44mRaY0k6AoEVn0jL41ywgO4dELjTFc7/tQlxSIBDbdRZdOjlI7McW3uDYKS3PvPEzhP4tRY/eamMNO0wVMrS5ZTHLS9XJJfZ6xo80HlHSIjaVjmB2TRqUnRGf8cY6Zqp89yUVGVp4dbeqtYt/qSMCyZOvWeTjYlFUXaioQxtL1wZsBhzbOx2grxO+0GQN4UMqbBg8ditSyK+WD0xKg6g0= admin@DESKTOP-5UHK4VD"
  }
  os_disk {
    caching           = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}

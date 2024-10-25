provider "azurerm" {
  features {}

  subscription_id = "b9e51426-d186-4d14-97ad-96ff7d42c978"
}
resource "azurerm_resource_group" "test" {
  name     = var.resource_group
  location = var.location
}

resource "azurerm_virtual_network" "test" {
  name = "${var.prefix}-NET"
  # address_space = ["10.0.0.0/22"]
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name
}

resource "azurerm_subnet" "test" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.test.name
  virtual_network_name = azurerm_virtual_network.test.name
  address_prefixes     = [var.address_prefix]
}

resource "azurerm_public_ip" "test" {
  name                = "${var.prefix}-pubip"
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_network_security_group" "test" {
  name                = "${var.prefix}-nsg"
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name

  security_rule {
    name                       = "${var.prefix}-5000"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "5000"
    source_address_prefix      = var.address_prefix
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}
resource "azurerm_subnet_network_security_group_association" "test" {
  subnet_id                 = azurerm_subnet.test.id
  network_security_group_id = azurerm_network_security_group.test.id
}

resource "azurerm_network_interface" "test" {
  name                = "${var.prefix}-nic"
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.test.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.test.id
  }
}

resource "azurerm_linux_virtual_machine" "test" {
  name                  = "${var.prefix}-linux-VM"
  location              = azurerm_resource_group.test.location
  resource_group_name   = azurerm_resource_group.test.name
  # size                  = "Standard_DS1_v2"
  size                  = "Standard_B1s"
  admin_username        = "devopsagent"
  admin_password        = "DevOpsAgent@123"
  disable_password_authentication = false
  network_interface_ids = [
    azurerm_network_interface.test.id
  ]

  # admin_ssh_key {
  #   username   = var.admin_username
  #   public_key = file("~/.ssh/id_rsa.pub")
  # }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}

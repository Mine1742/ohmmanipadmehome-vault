#azure


#### Example with parameters and ternary expression(if:then:else)
----
param location string = 'eastus'

param storageAccountName string = 'toylaunch${uniqueString(resourceGroup().id)}'

param appServiceAppName string = 'toylaunch${uniqueString(resourceGroup().id)}'

@allowed([

  'nonprod'

  'prod'

])

param environmentType string

var appServicePlanName = 'toy-produce-launch-plan'
#### Ternary expression
var storageAccountSkuName = (environmentType == 'prod') ? 'Standard_GRS' : 'Standard_LRS'

var appServicePlanSkuName = (environmentType == 'prod') ? 'P2v3' : 'S1'

  

resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = {

  name: storageAccountName

  location: location

  sku: {

    name: storageAccountSkuName

  }

  kind: 'StorageV2'

  properties: {

    accessTier: 'Hot'

  }

}

resource appServicePlan 'Microsoft.Web/serverfarms@2024-04-01' = {

  name: appServicePlanName

  location: location

  sku: {

    name: appServicePlanSkuName

  }

}

  

resource appServiceApp 'Microsoft.Web/sites@2024-04-01' = {

  name: appServiceAppName

  location: location

  properties: {

    serverFarmId: appServicePlan.id

    httpsOnly: true

  }

}

--------
####  To define an output in a Bicep file, use the `output` keyword like this:
output appServiceAppName string = appServiceAppName

output ipFqdn string = publicIPAddress.properties.dnsSettings.fqdn


### Modules
Bicep modules allow you to organize and reuse your Bicep code by creating smaller units that can be composed into a Bicep file. Any Bicep file can be used as a module by another template.

When you want the Bicep file to include a reference to a module file, use the `module` keyword. A module definition looks similar to a resource declaration, but instead of including a resource type and API version, you'll use the module's file name:

module myModule 'modules/mymodule.bicep' = {
  name: 'MyModule'
  params: {
    location: location
  }
}


https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep

https://learn.microsoft.com/en-us/azure/templates/

https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/bicep-functions

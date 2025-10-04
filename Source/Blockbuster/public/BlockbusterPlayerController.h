// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "BlockbusterPlayerController.generated.h"

class UInputMappingContext;
class UUserWidget;

UCLASS(abstract)
class BLOCKBUSTER_API ABlockbusterPlayerController : public APlayerController
{
	GENERATED_BODY()

public:

	/** Constructor */
	ABlockbusterPlayerController();

protected:

	/** Input Mapping Contexts */
	UPROPERTY(EditAnywhere, Category = "Input|Input Mappings")
	TArray<UInputMappingContext*> DefaultMappingContexts;

	/** Gameplay initialization */
	virtual void BeginPlay() override;

	/** Input mapping context setup */
	virtual void SetupInputComponent() override;

};

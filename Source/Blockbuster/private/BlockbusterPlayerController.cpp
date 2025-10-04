// Copyright Epic Games, Inc. All Rights Reserved.


#include "BlockbusterPlayerController.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/LocalPlayer.h"
#include "InputMappingContext.h"
#include "BlockbusterCameraManager.h"
#include "Blueprint/UserWidget.h"
#include "Blockbuster.h"

ABlockbusterPlayerController::ABlockbusterPlayerController()
{
	// set the player camera manager class
	PlayerCameraManagerClass = ABlockbusterCameraManager::StaticClass();
}

void ABlockbusterPlayerController::BeginPlay()
{
	Super::BeginPlay();
}

void ABlockbusterPlayerController::SetupInputComponent()
{
	Super::SetupInputComponent();

	// only add IMCs for local player controllers
	if (IsLocalPlayerController())
	{
		// Add Input Mapping Context
		if (UEnhancedInputLocalPlayerSubsystem* Subsystem = ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(GetLocalPlayer()))
		{
			for (UInputMappingContext* CurrentContext : DefaultMappingContexts)
			{
				Subsystem->AddMappingContext(CurrentContext, 0);
			}
		}
	}
}

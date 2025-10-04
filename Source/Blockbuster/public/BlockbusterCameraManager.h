// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Camera/PlayerCameraManager.h"
#include "BlockbusterCameraManager.generated.h"

UCLASS()
class ABlockbusterCameraManager : public APlayerCameraManager
{
	GENERATED_BODY()

public:

	/** Constructor */
	ABlockbusterCameraManager();
};
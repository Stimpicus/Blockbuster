// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Logging/LogMacros.h"
#include "BlockbusterCharacter.generated.h"

class UInputComponent;
class USkeletalMeshComponent;
class UCameraComponent;
class UInputAction;
struct FInputActionValue;

DECLARE_LOG_CATEGORY_EXTERN(LogBlockbusterCharacter, Log, All);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FSprintStateChangedDelegate, bool, bSprinting);

UCLASS(abstract)
class ABlockbusterCharacter : public ACharacter
{
	GENERATED_BODY()

	// Pawn mesh: first person view (arms; seen only by self)
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components", meta = (AllowPrivateAccess = "true"))
	USkeletalMeshComponent* FirstPersonMesh;

	// First person camera
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components", meta = (AllowPrivateAccess = "true"))
	UCameraComponent* FirstPersonCameraComponent;

public:
	ABlockbusterCharacter();

	// Replicate to everyone
	virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

	// Returns the first person mesh
	USkeletalMeshComponent* GetFirstPersonMesh() const { return FirstPersonMesh; }

	// Returns first person camera component
	UCameraComponent* GetFirstPersonCameraComponent() const { return FirstPersonCameraComponent; }

	// Delegate called when we start and stop sprinting
	FSprintStateChangedDelegate OnSprintStateChanged;

protected:
	// Set default sprint state
	UPROPERTY(Replicated)
	bool bSprinting = false;

	// Set default walk speed
	float WalkSpeed = 300.f;

	// Set default sprint speed
	float SprintSpeed = 600.f;

	// Sprint input action
	UPROPERTY(EditAnywhere, Category = "Input")
	UInputAction* SprintAction;

	// Jump input Action
	UPROPERTY(EditAnywhere, Category = "Input")
	UInputAction* JumpAction;

	// Move input Action
	UPROPERTY(EditAnywhere, Category = "Input")
	UInputAction* MoveAction;

	// Look input Action
	UPROPERTY(EditAnywhere, Category = "Input")
	class UInputAction* LookAction;

	// Mouse look input Action
	UPROPERTY(EditAnywhere, Category = "Input")
	class UInputAction* MouseLookAction;

	// Called from input actions for movement input
	void MoveInput(const FInputActionValue& Value);

	// Called from input actions for looking input
	void LookInput(const FInputActionValue& Value);

	// Handles aim inputs from either controls or UI interfaces
	UFUNCTION(BlueprintCallable, Category = "Input")
	virtual void DoAim(float Yaw, float Pitch);

	// Handles move inputs from either controls or UI interfaces
	UFUNCTION(BlueprintCallable, Category = "Input")
	virtual void DoMove(float Right, float Forward);

	// Handles jump start inputs from either controls or UI interfaces
	UFUNCTION(BlueprintCallable, Category = "Input")
	virtual void DoJumpStart();

	// Handles jump end inputs from either controls or UI interfaces
	UFUNCTION(BlueprintCallable, Category = "Input")
	virtual void DoJumpEnd();

	// Start sprinting
	UFUNCTION(BlueprintCallable, Category = "Input")
	void DoStartSprint();
	UFUNCTION(Server, Reliable)
	void Server_StartSprint();

	// Stop sprinting
	UFUNCTION(BlueprintCallable, Category = "Input")
	void DoEndSprint();
	UFUNCTION(Server, Reliable)
	void Server_StopSprint();

	// Set up input action bindings
	virtual void SetupPlayerInputComponent(UInputComponent* InputComponent) override;

	// Gameplay initialization
	virtual void BeginPlay() override;
};


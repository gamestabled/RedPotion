#include "Game/MapObj/NoteObj.h"
#include "Game/MapObj/CoinRotater.h"
#include "al/LiveActor/ActorPoseKeeper.h"
#include "al/LiveActor/LiveActorFunction.h"
#include "al/Placement/PlacementFunction.h"
#include "al/Scene/SceneObjHolder.h"

#ifdef NON_MATCHING // sucky sead inlines
NoteObj::NoteObj(const char* name)
    : MapObjActor(name)
    , mStartQuat(sead::Quatf::unit)
    , _70(false)
    , _71(true)
    , _74(-1)
    , _78(sead::Vector3f::zero)
    , mGenerator(nullptr)
{
    rp::createCoinRotater();
}

NoteObj::NoteObj(NoteObjGenerator* generator)
    : MapObjActor("�����I�u�W�F")
    , mStartQuat(sead::Quatf::unit)
    , _70(false)
    , _71(true)
    , _74(-1)
    , _78(sead::Vector3f::zero)
    , mGenerator(generator)
{
    rp::createCoinRotater();
}

extern "C" void FUN_00270fc4(al::LiveActor*, float); // MtxConnector (?)

static const char* sNoteObjArchive = "NoteObj";

void NoteObj::init(const al::ActorInitInfo& info) // STUPID sead inlines
{
    if (al::isPlaced(info)) {
        al::initActorWithArchiveName(this, info, sNoteObjArchive);
        mStartQuat = al::getQuat(this);
        FUN_00270fc4(this, 70.0);
        _78 = al::getTrans(this);
        al::invalidateClipping(this);
    }
    al::initActorWithArchiveNameNoPlacementInfo(this, info, sNoteObjArchive);
    makeActorDead();
}

void NoteObj::initAfterPlacement() { }
bool NoteObj::receiveMsg(u32 msg, al::HitSensor* other, al::HitSensor* me) { }

// creates new path instead of conditional instructions
void NoteObj::control()
{
    if (!_71)
        al::addVelocityToGravity(this, 0.5);
    al::rotateQuatYDirDegree(this, mStartQuat, rp::getCoinRotateY());
}
#endif
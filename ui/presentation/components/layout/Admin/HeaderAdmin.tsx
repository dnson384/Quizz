"use client";
import Image from "next/image";

import useNavigationBarAdmin from "@/presentation/hooks/Layout/Admin/useHeaderAdmin";
import useAuth from "@/presentation/hooks/Auth/useAuth";

export default function HeaderAdmin() {
  const {
    user,
    isFocused,
    keyword,
    inputRef,
    showUserMenu,
    userMenuRef,
    avatarRef,
    setIsFocused,
    handleMenuIcon,
    handleSearchInputFocus,
    handleSearchInputChange,
    handleSubmitSearchForm,
    handleLogoClick,
    handleUserAvatarClick,
    handlePersonalInformationClick,
  } = useNavigationBarAdmin();

  const { logoutUser } = useAuth();

  return (
    <>
      {user && (
        <>
          <nav className="pl-4 pr-6 py-4 flex justify-between items-center">
            {/* Menu & Logo */}
            <div className="flex items-center gap-3">
              <div
                className="p-2 cursor-pointer hover:bg-gray-200 hover:rounded-full"
                onClick={handleMenuIcon}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                >
                  <g fill="none">
                    <path d="m12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.018-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z" />
                    <path
                      fill="#2b303e"
                      d="M20 18a1 1 0 0 1 .117 1.993L20 20H4a1 1 0 0 1-.117-1.993L4 18zm0-7a1 1 0 1 1 0 2H4a1 1 0 1 1 0-2zm0-7a1 1 0 1 1 0 2H4a1 1 0 0 1 0-2z"
                    />
                  </g>
                </svg>
              </div>

              <h1
                className="text-3xl font-bold text-indigo-500 select-none cursor-pointer"
                onClick={handleLogoClick}
              >
                Quizz
              </h1>
            </div>

            {/* Search bar */}
            <form
              id="search-container"
              className={`w-2xl bg-gray-50 py-2 px-4 rounded-lg flex items-center gap-2 transition-all duration-200 border ${
                isFocused ? "border-indigo-500" : "border-gray-200"
              }`}
              onClick={handleSearchInputFocus}
              onSubmit={handleSubmitSearchForm}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
              >
                <path
                  fill="#2b303e"
                  d="M21.71 20.29L18 16.61A9 9 0 1 0 16.61 18l3.68 3.68a1 1 0 0 0 1.42 0a1 1 0 0 0 0-1.39M11 18a7 7 0 1 1 7-7a7 7 0 0 1-7 7"
                />
              </svg>
              <input
                id="search-bar"
                className="w-full focus:outline-0"
                ref={inputRef}
                type="text"
                placeholder="Tìm tài khoản người dùng"
                value={keyword || ""}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                onChange={handleSearchInputChange}
              />
            </form>

            {/* Create course & Account */}
            <div className="flex gap-3 items-center">
              {/* Create */}
              <div className="bg-indigo-500 w-9 h-9 flex items-center justify-center rounded-full cursor-pointer hover:bg-indigo-700">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="18"
                  height="18"
                  viewBox="0 0 256 256"
                >
                  <path
                    fill="#ffffff"
                    d="M228 128a12 12 0 0 1-12 12h-76v76a12 12 0 0 1-24 0v-76H40a12 12 0 0 1 0-24h76V40a12 12 0 0 1 24 0v76h76a12 12 0 0 1 12 12"
                  />
                </svg>
              </div>

              {/* Accout */}
              <div ref={avatarRef}>
                {user ? (
                  <Image
                    src={`/api/images${user.avatarUrl}`}
                    alt={user.name || "user avatar"}
                    width={36}
                    height={36}
                    className="w-9 h-9 rounded-full cursor-pointer"
                    onClick={handleUserAvatarClick}
                  ></Image>
                ) : (
                  <div className="w-9 h-9 rounded-full cursor-pointer bg-gray-300"></div>
                )}
              </div>
            </div>
          </nav>
          {showUserMenu && (
            <aside
              ref={userMenuRef}
              className="absolute right-6 rounded-xl shadow-[0_0_10px_rgba(0,0,0,0.3)]"
            >
              <div
                className="px-5 py-3 flex items-center gap-2 select-none cursor-pointer hover:bg-gray-200"
                onClick={handlePersonalInformationClick}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                >
                  <g
                    fill="none"
                    stroke="#374151"
                    strokeLinecap="round"
                    strokeWidth="2"
                  >
                    <path d="M19.727 20.447c-.455-1.276-1.46-2.403-2.857-3.207S13.761 16 12 16s-3.473.436-4.87 1.24s-2.402 1.931-2.857 3.207" />
                    <circle cx="12" cy="8" r="4" />
                  </g>
                </svg>
                <p className="font-semibold text-gray-700">Thông tin cá nhân</p>
              </div>
              <div
                className="px-5 py-3 flex items-center gap-2 select-none cursor-pointer hover:bg-gray-200"
                onClick={logoutUser}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                >
                  <path
                    fill="#374151"
                    d="M12 3.25a.75.75 0 0 1 0 1.5a7.25 7.25 0 0 0 0 14.5a.75.75 0 0 1 0 1.5a8.75 8.75 0 1 1 0-17.5"
                  />
                  <path
                    fill="#374151"
                    d="M16.47 9.53a.75.75 0 0 1 1.06-1.06l3 3a.75.75 0 0 1 0 1.06l-3 3a.75.75 0 1 1-1.06-1.06l1.72-1.72H10a.75.75 0 0 1 0-1.5h8.19z"
                  />
                </svg>
                <p className="font-semibold text-gray-700">Đăng xuất</p>
              </div>
            </aside>
          )}
        </>
      )}
    </>
  );
}
